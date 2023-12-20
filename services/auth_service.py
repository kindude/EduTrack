import uuid

from sqlalchemy.exc import IntegrityError
from constants.http_headers import HttpHeaders
from helpers.password_helper import PasswordHelper
from repositories.refresh_token import RefreshTokenRepository
from repositories.users import UsersRepository
from schemas.token import Token, TokenRefreshNotFoundException
from schemas.user import UserNotFoundException, WrongPasswordException, UserLogin, \
    UserExistsException, User, UserAddRequest
from services.token import JwtProcessorSingleton


class AuthService:

    def __init__(self, users_repo: UsersRepository, refresh_token_repo: RefreshTokenRepository):
        self.users_repo = users_repo
        self.password_helper = PasswordHelper()
        self.jwt_processor = JwtProcessorSingleton(session=self.users_repo.session)
        self.refresh_token_repo = refresh_token_repo
        self.http_headers = HttpHeaders()

    async def register_user(self, user_add: UserAddRequest) -> None:
        try:
            user = User(
                id=uuid.uuid4(),
                first_name=user_add.first_name,
                last_name=user_add.last_name,
                phone_number=user_add.phone_number,
                city=user_add.city,
                address=user_add.address,
                email=user_add.email,
                password_hash=self.password_helper.hash_password(user_add.password),
                role=user_add.role
            )

            await self.users_repo.add(user=user)
        except IntegrityError as exc:
            raise UserExistsException from exc

    async def login(self, user_to_login: UserLogin) -> Token:
        user = await self.users_repo.get_by_email(email=user_to_login.email)
        if not user:
            raise UserNotFoundException
        if not self.password_helper.check_password(login_password=user_to_login.password,
                                                   password=user.password_hash):
            raise WrongPasswordException
        access_token, token_id = self.jwt_processor.access_jwt_processor.generate(
            user_id=user.id, role=user.role.value)
        refresh_token, token_id = self.jwt_processor.refresh_jwt_processor.generate(
            user_id=user.id, role=user.role.value
        )
        await self.refresh_token_repo.save_item(token_id)
        return Token(access_token=access_token,
                     refresh_token=refresh_token,
                     type="bearer"
                     )

    async def refresh(self, request: Token) -> Token:
        refresh_token = self.jwt_processor.refresh_jwt_processor.decode(request.refresh_token)
        result = await self.refresh_token_repo.get_item(refresh_token.token_id)
        if result:
            access_token, token_id = self.jwt_processor.access_jwt_processor.generate(
                user_id=refresh_token.user_id,
                role=refresh_token.role
            )
            return Token(
                access_token=access_token,
                refresh_token=request.refresh_token,
                type="bearer"
            )

        raise TokenRefreshNotFoundException

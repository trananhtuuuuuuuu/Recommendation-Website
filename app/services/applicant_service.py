from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
#from app.core.exceptions import BusinessException # Your global exception
from app.mappers.mapper_applicant import MapperApplicant
from app.schemas.request.user.applicant import applicant_registration_request

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ApplicantService:
    @staticmethod
    def create_applicant(db: Session, request: applicant_registration_request):
      # 1. Business Logic: Check for duplicate User/Email
      existing_user = db.query(User).filter(
          (User.email == request.email) | (User.user_name == request.user_name)
      ).first()
      
      # if existing_user:
      #     # This triggers the Global Exception Handler automatically
      #     raise BusinessException(
      #         message="User with this email or username already exists", 
      #         status_code=409,
      #         error_code="DUPLICATE_USER"
      #     )

      # 2. Security: Hash the password before it touches the entity
      hashed_password = pwd_context.hash(request.password[:72])

      # 3. Use Mapper to convert Request -> Entity
      applicant_entity = MapperApplicant.map_request_to_entity(request)
        
      # 4. Overwrite plain password with the secure hash
      applicant_entity.user.password = hashed_password

      # 5. Database Persistence with safe transaction handling
      try:
        db.add(applicant_entity)
        db.flush()
        db.commit()
        db.refresh(applicant_entity)
      except Exception as e:
        db.rollback() # Important: Prevent partial saves if DB crashes
            #raise BusinessException(message="Internal Database Error", status_code=500)

        # 6. Use Mapper to convert Entity -> Response
      return MapperApplicant.map_entity_to_response(applicant_entity)
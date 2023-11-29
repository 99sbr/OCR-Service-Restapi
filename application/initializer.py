class LoggerInstance(object):
    def __new__(cls):
        from application.src.utility.logger.custom_logging import LogHandler
        return LogHandler()


class IncludeAPIRouter(object):
    def __new__(cls):
        from application.src.router.ocr import router as router_ocr_service
    
        from fastapi.routing import APIRouter
        router = APIRouter()
        router.include_router(router_ocr_service, prefix='/api/v1', tags=['OCR Service'])
        return router


# class DataBaseInstance(object):
#     def __new__(cls):
#         from application.main.infrastructure.database import db
#         return db.DataBase()


# instance creation
logger_instance = LoggerInstance()
# db_instance = DataBaseInstance()
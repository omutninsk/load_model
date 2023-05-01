"""Admin views."""

import uuid, datetime, os, math, shutil, json
import pickle
import pandas as pd
from flask import Blueprint, request, send_from_directory, current_app
from flask.views import MethodView
from sqlalchemy.orm import session
from sqlalchemy.sql import select, desc

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

from . import service as model_service
from models import schema as base_schemas
from tools.flasgger_marshmallow import swagger_decorator
from session import session_scope

model_blueprint = Blueprint('model', __name__)


class Fetch(MethodView):
    @swagger_decorator(query_schema=base_schemas.GetByIdQuerySchema, response_schema={400: base_schemas.ErrorResponseSchema})
    def get(self):
        """Обработка логов."""
        id= request.query_schema["id"]
        with session_scope() as session:
            res, source = model_service.fetch(session, id)
            return {"items": res, "source": source}

class Fit(MethodView):
    @swagger_decorator(query_schema=base_schemas.GetByIdQuerySchema, response_schema={400: base_schemas.ErrorResponseSchema})
    def get(self):
        """Обучение модели."""
        id= request.query_schema["id"]
        with session_scope() as session:
            res = model_service.fit(session, id)
        df = pd.DataFrame.from_records(res)
        #df.fillna(0, inplace=True)
        df = model_service.encode_column('additional', df)
        data = model_service.add_parallel_processes(df)
        
        y = data['duration']
        data.drop(['duration'], axis=1, inplace=True)

        # Создаем объект для преобразования данных
        poly = PolynomialFeatures(degree=2)

        # Преобразуем признаки
        X_poly = poly.fit_transform(data)

        X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)

        print('R^2 score:', r2)

        return {"items": res }

model_blueprint.add_url_rule('/fetch/', view_func=Fetch.as_view("fetch_api"))
model_blueprint.add_url_rule('/fit/', view_func=Fit.as_view("fit_api"))
# warehouse_test

## database.py

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
```

```SQLALCHEMY_DATABASE_URL:``` Строка подключения к базе данных SQLite. Здесь используется относительный
путь ```./test.db```, что
означает, что файл базы данных будет храниться в том же каталоге, что и исполняемый скрипт. Это указывает на
использование SQLite как базы данных. Строка подключения может меняться в зависимости от используемой СУБД

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
```

- ```engine```: Это объект "двигателя" (engine), который SQLAlchemy использует для подключения к базе данных и
  выполнения
  SQL-запросов.
- ```create_engine()```: Создаёт этот объект на основе строки подключения.
    - ```SQLALCHEMY_DATABASE_URL```: Передаётся как параметр, чтобы SQLAlchemy знала, куда подключаться.
    - ```connect_args={"check_same_thread": False}```: Это специальный параметр для SQLite, который отключает проверку
      на
      использование одного и того же потока. По умолчанию SQLite требует, чтобы все запросы к базе данных выполнялись из
      одного потока, но этот аргумент отключает эту проверку, позволяя работать с базой данных из разных потоков.

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

- ```SessionLocal```: Это фабрика, которая создаёт новые сессии для взаимодействия с базой данных. Каждая сессия — это
  отдельное соединение с базой данных, которое используется для выполнения запросов и записи изменений.
- Параметры фабрики:
    - ```autocommit=False```: Устанавливает, что изменения не будут автоматически фиксироваться (коммититься) в базе
      данных. Это означает, что нужно вручную вызывать ```commit()```, чтобы сохранить изменения.
    - ```autoflush=False```: Отключает автоматическое "сбрасывание" изменений в базу данных перед каждым запросом. Это
      также означает, что изменения сохранятся только после явного вызова ```flush()``` или ```commit()```.
    - ```bind=engine```: Связывает сессию с двигателем базы данных, чтобы сессия знала, с какой базой данных работать.

```python
Base = declarative_base()
```

- ```Base```: Это базовый класс для всех моделей базы данных, которые вы будете создавать. Все ваши таблицы будут
  наследовать от этого класса. Он необходим для определения схемы таблиц в базе данных.

### Итог

- ```engine``` управляет подключением к базе данных.
- ```SessionLocal``` создаёт сессии, которые используются для выполнения запросов к базе данных.
- ```Base``` служит основой для определения моделей таблиц, которые будут использоваться для создания и взаимодействия с
  данными в базе данных

## models.py

```python
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    # Связь с OrderItem
    order_items = relationship("OrderItem", back_populates="product")
```

- **Связь:** Один ко многим
    - **Направление:** Один продукт может иметь много элементов заказа.
    - **Объяснение:** В этой модели связь устанавливается через атрибут ```order_items```, который представляет собой
      список всех элементов заказа ```(OrderItem)```, относящихся к данному продукту ```(Product)```. Это значит, что
      один и тот же продукт может появляться в разных заказах (например, "Товар A" может быть в Заказе 1 и Заказе 2).

```python
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, default=formatted_datetime)
    status = Column(String, index=True)

    order_items = relationship("OrderItem", back_populates="order")
```

- **Связь:** Один ко многим
    - **Направление:** Один заказ может содержать много элементов заказа.
    - **Объяснение:** Связь с моделью ```OrderItem``` осуществляется через атрибут ```order_items```, который является
      списком всех элементов заказа, принадлежащих этому заказу. Это значит, что в одном заказе (например, Заказ 1)
      могут быть несколько различных товаров (например, "Товар A", "Товар B").

```python
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
```

- **Связь:** Многие к одному
    - **Направление:** Много элементов заказа могут ссылаться на один заказ и один продукт.
    - **Объяснение:**
        - ```order```: Каждый элемент заказа связан с одним заказом. Это значит, что несколько элементов
          заказа ```(OrderItem)``` могут принадлежать одному и тому же заказу ```(Order)```.
        - ```product```: Каждый элемент заказа также связан с одним продуктом. Это означает, что несколько элементов
          заказа могут относиться к одному и тому же продукту.

### Общая структура и связи

- ```Product```:
    - Один ко многим к ```OrderItem```: Один продукт может иметь множество элементов заказа, относящихся к нему.
    - ```Order```: Один ко многим к ```OrderItem```: Один заказ может включать множество элементов заказа.
    - ```OrderItem```:
        - Многие к одному к ```Order```: Множество элементов заказа может ссылаться на один заказ.
        - Многие к одному к ```Product```: Множество элементов заказа может ссылаться на один продукт.

## schemas.py

- Эти модели предоставляют удобный способ описать данные, связанные с продуктами и заказами, и использовать валидацию
  входных данных.
- Используя Pydantic, можно легко проверять и преобразовывать данные, что полезно при работе с API и хранении данных в
  базах данных


## products.py
```python
router = APIRouter()
```
- Создает новый экземпляр ```APIRouter```, который будет использоваться для определения маршрутов.
```python
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- ```get_db():``` Эта функция создает и возвращает сессию базы данных.
- ```yield db:``` Возвращает сессию, чтобы ее можно было использовать в маршрутах.
- ```finally: db.close(): ``` Закрывает сессию после использования, чтобы избежать утечек ресурсов.


```python
@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
```

- ```@router.post("/")```: Определяет маршрут для POST-запроса на создание нового продукта.
- ```create_product()```: Функция, которая обрабатывает запрос.
  - ```product: schemas.ProductCreate```: Принимает данные о продукте, валидируемые с помощью ```Pydantic```.
  - Создает новый экземпляр ```models.Product```, заполняя его данными из схемы.
  - Добавляет продукт в сессию, коммитит изменения и обновляет объект с идентификатором, созданным в базе данных.
  - Возвращает созданный продукт.

```python
@router.get("/", response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products
```

- ```@router.get("/")```: Определяет маршрут для GET-запроса на получение списка всех продуктов.
- ```get_products()```: Функция, которая обрабатывает запрос.
  - Использует сессию базы данных и выполняет запрос к таблице ```Product```, чтобы получить все продукты.
  - Возвращает список продуктов.

```python
@router.get("/{id}", response_model=schemas.Product)
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
```

- ```@router.get("/{id}")```: Определяет маршрут для GET-запроса на получение продукта по его идентификатору.
- ```get_product()```: Функция, которая обрабатывает запрос.
  - Выполняет запрос к таблице ```Product```, чтобы найти продукт с указанным ID.
  - Если продукт не найден, генерируется ```HTTPException``` с кодом 404.
  - Возвращает найденный продукт.

```python
@router.put("/{id}", response_model=schemas.Product)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product
```

- ```@router.put("/{id}")```: Определяет маршрут для PUT-запроса на обновление существующего продукта.
- ```update_product()```: Функция, которая обрабатывает запрос.
  - Выполняет запрос к таблице ```Product```, чтобы найти продукт с указанным ID.
  - Если продукт не найден, генерируется ```HTTPException``` с кодом 404.
  - Обновляет поля продукта с помощью переданных данных.
  - Коммитит изменения и возвращает обновленный продукт.

```python
@router.delete("/{id}", response_model=dict)
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
```

- ```@router.delete("/{id}")```: Определяет маршрут для DELETE-запроса на удаление продукта.
- ```delete_product()```: Функция, которая обрабатывает запрос.
  - Выполняет запрос к таблице ```Product```, чтобы найти продукт с указанным ID.
  - Если продукт не найден, генерируется ```HTTPException``` с кодом 404.
  - Удаляет продукт из базы данных и коммитит изменения.
  - Возвращает сообщение о том, что продукт был удален.


### Общая структура
- **Создание**: Создает новый продукт в базе данных.
- **Получение**: Получает список всех продуктов или конкретный продукт по ID.
- **Обновление**: Обновляет существующий продукт.
- **Удаление**: Удаляет продукт из базы данных.

## main.py

```python
database.Base.metadata.drop_all(bind=database.engine)
database.Base.metadata.create_all(bind=database.engine)
```

- ```drop_all```: Удаляет все таблицы в базе данных, которые были определены в моделях данных.
- ```create_all```: Создает таблицы в базе данных на основе определенных моделей данных. Это полезно для инициализации базы данных с нуля, особенно в процессе разработки.

```python
app = FastAPI()
```
- Создает экземпляр приложения FastAPI.

```python
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
```

- Подключает маршрутизаторы к приложению, добавляя префиксы к URL. Например, все эндпоинты, определенные в ```products_router```, будут доступны по пути ```/products```, а в ```orders_router``` — по пути ```/orders```. Теги помогают в документации API.

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

- Проверяет, запущен ли скрипт непосредственно (а не импортирован как модуль в другой код). Если это так, запускает сервер Uvicorn, который позволяет обращаться к приложению FastAPI. Приложение будет доступно на ```http://127.0.0.1:8000```.


## test_api.py

```python
client = TestClient(app)
```
- Создается экземпляр ```TestClient```, связанный с вашим приложением FastAPI, что позволяет выполнять запросы к API в тестах.

```python
def test_create_product():
    product_data = {
        "title": "Продукт_тест_",
        "description": "Продукт_тест_",
        "price": 20.01,
        "stock": 100
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == product_data["title"]
    assert response_data["description"] == product_data["description"]
    assert response_data["price"] == product_data["price"]
    assert response_data["stock"] == product_data["stock"]
```

- **Функция** ```test_create_product()```: Этот тест проверяет, что продукт может быть успешно создан с корректными данными.
- ```product_data```: Словарь с данными нового продукта, который будет отправлен в запросе.
- ```response = client.post("/products/", json=product_data)```: Отправляет POST-запрос на эндпоинт ```/products/```, передавая данные продукта в формате JSON.
- ```assert response.status_code == 200```: Проверяет, что статус ответа равен 200 (успешное выполнение).
- ```response_data = response.json()```: Получает данные из ответа в формате JSON.
- Проверяются значения, чтобы убедиться, что они соответствуют отправленным данным.

```python
def test_create_product_missing_fields():
    product_data = {
        "title": "Test Product"
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == 422
    assert "detail" in response.json()
```

- **Функция** ```test_create_product_missing_fields()```: Этот тест проверяет, как API обрабатывает запрос на создание продукта, если некоторые обязательные поля отсутствуют.
- ```product_data```: Словарь с неполными данными (отсутствуют поля description, price и stock).
- ```response = client.post("/products/", json=product_data)```: Отправляет POST-запрос с неполными данными.
- ```assert response.status_code == 422```: Проверяет, что статус ответа равен 422 (неверный запрос), что указывает на ошибки валидации.
- ```assert "detail" in response.json()```: Убедитесь, что в ответе есть поле "detail", которое содержит информацию об ошибке.

```python
def test_get_products():
    response = client.get("/products/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
```

- **Функция** ```test_get_products()```: Этот тест проверяет, что можно получить список всех продуктов.
- ```response = client.get("/products/")```: Отправляет GET-запрос на эндпоинт /products/, чтобы получить список продуктов.
- ```assert response.status_code == 200```: Проверяет, что статус ответа равен 200 (успешное выполнение).
- ```response_data = response.json()```: Получает данные из ответа в формате JSON.
- ```assert isinstance(response_data, list)```: Проверяет, что данные, возвращенные в ответе, представляют собой список.
"""
🔐 Потокобезопасный Singleton для подключения к БД
Все классы в одном файле для наглядности
"""

import threading
from typing import Optional


# =============================================================================
# 🔐 Метакласс для потокобезопасного Singleton (Double-Checked Locking)
# =============================================================================
class SingletonMeta(type):
    """
    Потокобезопасный метакласс реализации Singleton.
    Использует double-checked locking для минимизации накладных расходов.
    """
    _instances = {}
    _lock: threading.Lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        # Первый check без блокировки (для производительности)
        if cls not in cls._instances:
            with cls._lock:
                # Второй check внутри блокировки (для безопасности)
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


# =============================================================================
# 🗄️ Класс подключения к БД (Singleton)
# =============================================================================
class DatabaseConnection(metaclass=SingletonMeta):
    """
    Подключение к базе данных как Singleton.
    Гарантирует один экземпляр на всё приложение.
    """
    
    def __init__(self, url: str):
        # 🛡️ Защита от повторной инициализации
        # (т.к. __init__ вызывается каждый раз при обращении к Singleton)
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.url = url
        self._connection: Optional[object] = None
        
        print(f"✅ [DB] Создано подключение к {url}")
        self._init_connection()
        
        self._initialized = True
    
    def _init_connection(self):
        """Тяжелая инициализация: драйвер, auth, handshake..."""
        # Симуляция дорогой операции
        threading.Event().wait(0.01)  # имитация задержки
        self._connection = f"Connection({self.url})"
    
    def query(self, sql: str) -> dict:
        """Выполнение SQL-запроса"""
        print(f"🔍 [DB] Запрос: {sql}")
        # Симуляция выполнения
        return {"status": "ok", "rows": []}
    
    def close(self):
        """Закрытие подключения (вызывать при завершении приложения)"""
        if hasattr(self, '_initialized') and self._initialized:
            print(f"🔌 [DB] Закрытие подключения к {self.url}")
            self._connection = None
    
    # Для отладки: проверка, что это тот же экземпляр
    def get_instance_id(self) -> int:
        return id(self)


# =============================================================================
# 👥 Сервисы приложения (клиентский код)
# =============================================================================
class UserService:
    """Сервис работы с пользователями"""
    
    def create_user(self, name: str) -> dict:
        # ✅ Получаем тот же экземпляр подключения
        conn = DatabaseConnection("jdbc:mysql://localhost/mydb")
        result = conn.query(f"INSERT INTO users (name) VALUES ('{name}')")
        print(f"   👤 Пользователь '{name}' создан")
        return result
    
    def get_user(self, user_id: int) -> dict:
        conn = DatabaseConnection("jdbc:mysql://localhost/mydb")
        return conn.query(f"SELECT * FROM users WHERE id={user_id}")


class OrderService:
    """Сервис работы с заказами"""
    
    def create_order(self, user_id: int, items: list) -> dict:
        # ✅ То же самое подключение, что и в UserService!
        conn = DatabaseConnection("jdbc:mysql://localhost/mydb")
        result = conn.query(
            f"INSERT INTO orders (user_id, items) VALUES ({user_id}, '{items}')"
        )
        print(f"   📦 Заказ для user_id={user_id} создан")
        return result


# =============================================================================
# 🚀 Точка входа
# =============================================================================
def main():
    print("🎬 Запуск приложения...\n")
    
    # Создаём сервисы
    user_service = UserService()
    order_service = OrderService()
    
    # Проверяем, что подключение создаётся только один раз
    print("─" * 60)
    print("1️⃣  Создаём пользователя:")
    user_service.create_user("Alice")
    id_1 = DatabaseConnection("jdbc:mysql://localhost/mydb").get_instance_id()
    
    print("\n2️⃣  Создаём заказ:")
    order_service.create_order(user_id=1, items=["item1", "item2"])
    id_2 = DatabaseConnection("jdbc:mysql://localhost/mydb").get_instance_id()
    
    print("\n3️⃣  Ещё один запрос от UserService:")
    user_service.get_user(1)
    id_3 = DatabaseConnection("jdbc:mysql://localhost/mydb").get_instance_id()
    
    # 🔍 Валидация Singleton
    print("\n" + "─" * 60)
    print("🔐 Проверка Singleton:")
    print(f"   ID экземпляра #1: {id_1}")
    print(f"   ID экземпляра #2: {id_2}")
    print(f"   ID экземпляра #3: {id_3}")
    
    if id_1 == id_2 == id_3:
        print("   ✅ ВСЕ ССЫЛКИ УКАЗЫВАЮТ НА ОДИН ОБЪЕКТ (Singleton работает!)")
    else:
        print("   ❌ ОШИБКА: создано несколько экземпляров!")
    
    # Закрытие подключения при завершении
    print("\n🏁 Завершение работы:")
    DatabaseConnection("jdbc:mysql://localhost/mydb").close()


# =============================================================================
# 🧪 Тест потокобезопасности (опционально)
# =============================================================================
def test_thread_safety():
    """Проверка, что Singleton работает в многопоточной среде"""
    print("\n🧪 Тест потокобезопасности (10 потоков)...")
    
    instance_ids = []
    lock = threading.Lock()
    
    def worker(thread_num: int):
        conn = DatabaseConnection("jdbc:mysql://localhost/mydb")
        with lock:
            instance_ids.append((thread_num, id(conn)))
        # Имитация работы
        threading.Event().wait(0.01)
    
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    unique_ids = set(obj_id for _, obj_id in instance_ids)
    
    print(f"   📊 Уникальных экземпляров: {len(unique_ids)} (ожидалось: 1)")
    if len(unique_ids) == 1:
        print("   ✅ Потокобезопасность подтверждена!")
    else:
        print("   ❌ ОШИБКА: нарушение потокобезопасности!")


# =============================================================================
# ▶️ Запуск
# =============================================================================
if __name__ == "__main__":
    main()
    test_thread_safety()
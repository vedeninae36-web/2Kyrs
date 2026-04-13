java
// Проблема: Менеджер подключения к БД создается в разных местах
class DatabaseConnection {
    private String url;
    
    public DatabaseConnection(String url) {
        this.url = url;
        System.out.println("Создано новое подключение к " + url);
        // Реальная инициализация (тяжелая)
    }
    
    public void query(String sql) {
        System.out.println("Выполнение запроса: " + sql);
    }
}

// Клиентский код
class UserService {
    public void createUser(String name) {
        DatabaseConnection conn = new DatabaseConnection("jdbc:mysql://localhost/db");
        conn.query("INSERT INTO users ...");
    }
}

class OrderService {
    public void createOrder() {
        DatabaseConnection conn = new DatabaseConnection("jdbc:mysql://localhost/db");
        conn.query("INSERT INTO orders ...");
    }
}

// Использование
public class Main {
    public static void main(String[] args) {
        UserService userService = new UserService();
        OrderService orderService = new OrderService();
        
        userService.createUser("John");
        orderService.createOrder();
        // Будет создано два подключения к БД! (плохо для производительности)
    }
}

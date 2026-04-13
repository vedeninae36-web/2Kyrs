// Три сложных класса для работы с заказом
class InventorySystem {
    public boolean checkStock(String productId, int quantity) {
        System.out.println("Проверка наличия " + productId);
        return true;
    }
    public void reserveProduct(String productId, int quantity) {
        System.out.println("Резервирование " + productId);
    }
}

class PaymentSystem {
    public boolean processPayment(String orderId, double amount) {
        System.out.println("Обработка платежа " + amount);
        return true;
    }
    public void refund(String orderId) {
        System.out.println("Возврат платежа");
    }
}

class DeliverySystem {
    public void createDelivery(String orderId, String address) {
        System.out.println("Создание доставки по адресу: " + address);
    }
    public void trackDelivery(String orderId) {
        System.out.println("Отслеживание доставки");
    }
}

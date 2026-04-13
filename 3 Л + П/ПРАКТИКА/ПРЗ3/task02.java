// Проблема: Система уведомлений жестко привязана к типам
class NotificationService {
    
    public void sendNotification(String type, String message, String recipient) {
        if (type.equals("email")) {
            // Логика отправки email
            System.out.println("Отправка email на " + recipient + ": " + message);
        } else if (type.equals("sms")) {
            // Логика отправки SMS
            System.out.println("Отправка SMS на " + recipient + ": " + message);
        } else if (type.equals("telegram")) {
            // Логика отправки Telegram
            System.out.println("Отправка Telegram на " + recipient + ": " + message);
        }
        // При добавлении нового типа (whatsapp) придется менять этот метод!
    }
}

// Использование
public class Main {
    public static void main(String[] args) {
        NotificationService service = new NotificationService();
        service.sendNotification("email", "Привет!", "user@mail.com");
        service.sendNotification("sms", "Привет!", "+79123456789");
    }
}

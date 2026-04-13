// Проблема: Конструктор с множеством параметров
class HttpRequest {
    private String url;
    private String method;
    private String body;
    private String contentType;
    private int timeoutSeconds;
    private boolean followRedirects;
    private String authorizationToken;
    private String userAgent;
    
    // Ужасный конструктор с кучей параметров!
    public HttpRequest(String url, String method, String body, String contentType, 
                      int timeoutSeconds, boolean followRedirects, 
                      String authorizationToken, String userAgent) {
        this.url = url;
        this.method = method;
        this.body = body;
        this.contentType = contentType;
        this.timeoutSeconds = timeoutSeconds;
        this.followRedirects = followRedirects;
        this.authorizationToken = authorizationToken;
        this.userAgent = userAgent;
    }
    
    // Геттеры...
}

// Использование - невозможно запомнить порядок!
public class Main {
    public static void main(String[] args) {
        HttpRequest request = new HttpRequest(
            "https://api.example.com/users",
            "POST",
            "{\"name\":\"John\"}",
            "application/json",
            30,
            true,
            "Bearer token123",
            "MyApp/1.0"
        );
    }
}

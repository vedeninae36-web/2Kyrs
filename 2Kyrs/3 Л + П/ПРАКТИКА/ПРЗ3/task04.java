// Проблема: Есть старая библиотека для работы с XML, а новый код работает с JSON

// Старая библиотека (нельзя менять)
class XmlLibrary {
    public String getXmlData() {
        return "<user><name>John</name><age>30</age></user>";
    }
    
    public void processXml(String xml) {
        System.out.println("Обработка XML: " + xml);
    }
}

// Новый интерфейс, который ожидает клиент
interface JsonProcessor {
    String getJson();
    void processJson(String json);
}

// Клиентский код
class Client {
    public void work(JsonProcessor processor) {
        String json = processor.getJson();
        System.out.println("Клиент получил JSON: " + json);
        processor.processJson("{\"status\":\"ok\"}");
    }
}

using System.Text.Json.Serialization;

public class Weather
{
    [JsonPropertyName("temperature")]
    public double Temperature { get; set; }

    [JsonPropertyName("location")]
    public string? LocationName { get; set; }

    [JsonPropertyName("wind_speed")]
    public double WindSpeed { get; set; }

    [JsonPropertyName("wind_direction")]
    public int WindDirection { get; set; }

    [JsonPropertyName("conditions")]
    public string? CurrentConditions { get; set; }

    public static Weather FromJson(string json)
    {
        var weather = System.Text.Json.JsonSerializer.Deserialize<Weather>(json);
        return weather;
    }
}
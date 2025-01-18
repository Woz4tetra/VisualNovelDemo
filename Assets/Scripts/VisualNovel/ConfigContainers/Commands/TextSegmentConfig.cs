using System;

[Serializable]
public class TextSegmentConfig : CommandConfig
{
    public string text { get; set; }
    public string color { get; set; }
    public string[] styles { get; set; }
}

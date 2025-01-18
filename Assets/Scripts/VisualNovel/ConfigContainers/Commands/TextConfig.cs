using System;

[Serializable]
public class TextConfig : CommandConfig
{
    public string format { get; set; }
    public TextSegmentConfig[] segments { get; set; }
}

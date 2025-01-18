using System;

[Serializable]
public class DelayCommand : CommandConfig
{
    public float duration { get; set; }
}

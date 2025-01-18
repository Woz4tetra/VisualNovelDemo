using System;

[Serializable]
public class PlaySoundConfig : CommandConfig
{
    public string sound { get; set; }
    public float volume { get; set; }
}

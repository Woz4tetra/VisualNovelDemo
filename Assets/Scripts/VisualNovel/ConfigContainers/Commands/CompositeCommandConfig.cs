using System;

[Serializable]
public class CompositeCommandConfig : CommandConfig
{
    public CommandConfig[] subcommands { get; set; }
}

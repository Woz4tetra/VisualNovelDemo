from .composite_behavior import CompositeBehavior
from .delay_behavior import DelayBehavior
from .play_sound_behavior import PlaySoundBehavior
from .set_backdrop_behavior import SetBackdropBehavior
from .text_behavior import TextBehavior
from .transition_to_sequence_behavior import TransitionToSequenceBehavior

Behaviors = (
    SetBackdropBehavior,
    DelayBehavior,
    TransitionToSequenceBehavior,
    CompositeBehavior,
    PlaySoundBehavior,
    TextBehavior,
)
BehaviorType = (
    SetBackdropBehavior
    | DelayBehavior
    | TransitionToSequenceBehavior
    | CompositeBehavior
    | PlaySoundBehavior
    | TextBehavior
)

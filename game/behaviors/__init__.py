from .delay_behavior import DelayBehavior
from .set_backdrop_behavior import SetBackdropBehavior
from .transition_to_sequence_behavior import TransitionToSequenceBehavior

Behaviors = (
    SetBackdropBehavior,
    DelayBehavior,
    TransitionToSequenceBehavior,
)
BehaviorType = SetBackdropBehavior | DelayBehavior | TransitionToSequenceBehavior

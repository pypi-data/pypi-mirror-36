from emotion_data.plutchik import Emotion, EmotionalDimension, DIMENSIONS, Neutrality
from emotion_data.feelings import Feeling

from copy import copy
import numpy as np


COMPOSITE_EMOTIONS_NAMES = {
    "aggressiveness": ["rage", "vigilance"],
    "rejection": ["rage", "amazement"],
    "rivalry": ["rage", "admiration"],
    "contempt": ["rage", "loathing"],

    "anxiety": ["terror", "vigilance"],
    "awe": ["terror", "amazement"],
    "submission": ["terror", "admiration"],
    "coercion": ["terror", "loathing"],

    "optimism": ["ecstasy", "vigilance"],
    "frivolity": ["ecstasy", "amazement"],
    "love": ["ecstasy", "admiration"],
    "gloat": ["ecstasy", "loathing"],

    "frustration": ["grief", "vigilance"],
    "disapproval": ["grief", "amazement"],
    "envy": ["grief", "admiration"],
    "remorse": ["grief", "loathing"]
}

OPPOSITE_EMOTIONS_NAMES = {
    "annoyance": "apprehension",
    "interest": "distraction",
    "serenity": "pensiveness",
    "acceptance": "boredom",
    "trust": "disgust",
    "joy": "sadness",
    "anticipation": "surprise",
    "anger": "fear",
    "rage": "terror",
    "vigilance": "amazement",
    "ecstasy": "grief",
    "admiration": "loathing",
    "apprehension": "annoyance",
    "distraction": "interest",
    "pensiveness": "serenity",
    "boredom": "acceptance",
    "disgust": "trust",
    "sadness": "joy",
    "surprise": "anticipation",
    "fear": "anger",
    "terror": "rage",
    "amazement": "vigilance",
    "grief": "ecstasy",
    "loathing": "admiration",
    # composite
    "contempt": "submission",
    "rivalry": "coercion",
    "anxiety": "rejection",
    "awe": "aggressiveness",
    "love": "remorse",
    "envy": "gloat",
    "frivolity": "frustration",
    "disapproval": "optimism",
    "submission": "contempt",
    "coercion": "rivalry",
    "rejection": "anxiety",
    "aggressiveness": "awe",
    "remorse": "love",
    "gloat": "envy",
    "frustration": "frivolity",
    "optimism": "disapproval"
}


class CompositeEmotion(Emotion):
    sensitivity_dimension = DIMENSIONS["sensitivity"]
    attention_dimension = DIMENSIONS["attention"]
    pleasantness_dimension = DIMENSIONS["pleasantness"]
    aptitude_dimension = DIMENSIONS["aptitude"]

    def __init__(self, name=""):
        Emotion.__init__(self, name)
        self.components = []

    @staticmethod
    def get_composite_from_emotions(emotion1, emotion2):
        for c in COMPOSITE_EMOTIONS:
            emos = COMPOSITE_EMOTIONS[c]
            if emotion1 in emos and emotion2 in emos:
                return c
        return None

    @property
    def dimension(self):
        d = CompositeDimension()
        for dim in self.dimensions:
            d = d + dim
        return d

    @property
    def dimensions(self):
        return [e.dimension for e in self.components]

    @staticmethod
    def matrix_to_array(m):
        sensitivity = m.item(0, 0)
        attention = m.item(0, 1)
        pleasantness = m.item(1, 0)
        aptitude = m.item(1, 1)
        return np.array([sensitivity, attention, pleasantness, aptitude])

    @staticmethod
    def array_to_emotion(arr):
        sensitivity = Neutrality(dimension="sensitivity") + arr.item(0)
        attention = Neutrality(dimension="attention") + arr.item(1)
        pleasantness = Neutrality(dimension="pleasantness") + arr.item(2)
        aptitude = Neutrality(dimension="aptitude") + arr.item(3)
        return sensitivity + pleasantness + aptitude + attention

    @property
    def emotion_vector(self):
        sensitivity = Neutrality()
        attention = Neutrality()
        pleasantness = Neutrality()
        aptitude = Neutrality()
        for emotion in self.components:
            if emotion.dimension == self.sensitivity_dimension:
                sensitivity = sensitivity + emotion
            elif emotion.dimension == self.attention_dimension:
                attention = attention + emotion
            elif emotion.dimension == self.aptitude_dimension:
                aptitude = aptitude + emotion
            elif emotion.dimension == self.pleasantness_dimension:
                pleasantness = pleasantness + emotion

        return [sensitivity, attention, pleasantness, aptitude]

    @property
    def emotion_matrix(self):
        return self.as_matrix

    @property
    def name(self):
        name = ""
        if len(self.components) == 2:
            name = self.get_composite_from_emotions(self.components[0], self.components[1])
        return self._name or name or self.secondary_name

    @property
    def secondary_name(self):
        if len(self.components):
            name = ""
            for emo in self.components:
                dimension = emo.dimension.axis
                name += dimension + " of " + emo.name + ", "
            return name[:-2]

        return "neutrality"

    @property
    def type(self):
        # TODO science this instead of eye balling
        types = []
        valence = 0
        for dim in self.dimensions:
            if self.emotional_flow < 0:  # 2 x low
                if "attention" in dim.axis:
                    valence -= 1
                    if "not in control" not in types:
                        types.append("not in control")
                if "aptitude" in dim.axis:
                    valence -= 1
                    if "forceful" not in types:
                        types.append("forceful")
            elif self.emotional_flow == 0:  # low + high
                if "attention" in dim.axis:
                    valence -= 1
                    if "forceful" not in types:
                        types.append("forceful")

                if "aptitude" in dim.axis:
                    valence -= 1
                    if "not in control" not in types:
                        types.append("not in control")
            else:  # 2 x high
                if "aptitude" in dim.axis:
                    valence += 1
                    if "caring" not in types:
                        types.append("caring")
                if "sensitivity" in dim.axis:
                    valence -= 1
                    if "not in control" not in types:
                        types.append("not in control")
                if "pleasantness" in dim.axis:
                    valence += 1
                    if "quiet" not in types:
                        types.append("quiet")
        if valence:
            return "positive " + " and ".join(types)
        elif valence == 0:
            return "neutral " + " and ".join(types)
        return "negative " + " and ".join(types)

    @property
    def kind(self):
        # TODO science this instead of eye balling
        #for kind in EMOTION_KIND_NAMES:
        #    if self._name in EMOTION_KIND_NAMES[kind]:
        #        return kind
        return self._kind

    @property
    def base_emotion(self):
        c = CompositeEmotion()
        for e in self.emotion_vector:
            c = c + e
        return c

    @property
    def parent_emotion(self):
        return None

    @property
    def opposite_emotion(self):
        return self.__neg__()

    @property
    def emotional_flow(self):
        # scalar product
        flows = [e.emotional_flow for e in self.emotion_vector]
        flow_vector = np.array(flows)
        return np.linalg.norm(flow_vector)

    @property
    def is_composite(self):
        return True

    @property
    def equivalent_feeling(self):
        from emotion_data.feelings import Feeling
        if len(self.components) == 2:
            from emotion_data.feelings import FEELINGS_TO_EMOTION_MAP, FEELINGS
            for feel in FEELINGS_TO_EMOTION_MAP:
                # print(self.components[0].name, self.components[1].name)
                feel = feel.lower()
                if self.components[0].name in [f.name.lower() for f in FEELINGS_TO_EMOTION_MAP[feel]] and self.components[
                    1].name in [f.name.lower() for f in FEELINGS_TO_EMOTION_MAP[feel]]:
                    return copy(FEELINGS[feel])
        f = Feeling()
        f.emotions = self.components
        return f

    def __str__(self):
        return self.name

    def __repr__(self):
        return "CompositeEmotionObject:" + self.name

    def __neg__(self):
        vector = [- e for e in self.emotion_vector]
        c = CompositeEmotion()
        for e in vector:
            c = c + e
        return c

    def __add__(self, other):
        if isinstance(other, str):
            other = self.string_to_emotion(other)

        if isinstance(other, Neutrality):
            emo = copy(self)
            return emo

        if isinstance(other, Feeling):
            c = copy(self)
            for e in other.emotions:
                c = c + e
            return c

        if isinstance(other, Emotion):
            # matrix product of emotion vectors
            other_vector = other.emotion_vector

            result_vector = np.array(other_vector) + np.array(self.emotion_vector)
            c = CompositeEmotion()

            for e in result_vector:
                if e.dimension:
                    c.components.append(e)
            return c

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, str):
            other = self.string_to_emotion(other)

        if isinstance(other, Neutrality):
            emo = copy(self)
            return emo

        if isinstance(other, Feeling):
            c = copy(self)
            for e in other.emotions:
                c = c - e
            return c

        if isinstance(other, Emotion):
            # matrix product of emotion vectors
            other_vector = other.emotion_vector

            result_vector = np.array(other_vector) - np.array(self.emotion_vector)
            c = CompositeEmotion()

            for e in result_vector:
                if e.dimension:
                    c.components.append(e)
            if len(c.components) == 1:
                return c.components[0]
            if not len(c.components):
                return Neutrality()
            return c

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Neutrality):
            emo = copy(self)
            return emo
        if isinstance(other, Emotion):
            m = self.as_matrix * other.as_matrix

            return m
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, str):
            other = self.string_to_emotion(other)
        if isinstance(other, Neutrality):
            emo = copy(self)
            return emo
        elif isinstance(other, CompositeEmotion):
            pass
        elif isinstance(other, Emotion):
            emo = copy(self)
            if other in emo.components:
                emo.components.remove(other)
                return emo
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, str):
            other = self.string_to_emotion(other)
        if isinstance(other, Neutrality):
            emo = copy(self)
            return emo
        if isinstance(other, CompositeEmotion):
            pass
        elif isinstance(other, Emotion):
            emo = copy(self)
            if other in emo.components:
                emo.components.remove(other)
                return emo
        return NotImplemented

    def __lshift__(self, other):
        if isinstance(other, str):
            other = self.string_to_emotion(other)
        if isinstance(other, Neutrality):
            emo = copy(self)
            return emo
        return NotImplemented

    def __rshift__(self, other):
        if isinstance(other, str):
            other = self.string_to_emotion(other)
        if isinstance(other, Neutrality):
            emo = copy(self)
            return emo
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Emotion):
            return self.emotional_flow < other.emotional_flow
        return self.emotional_flow < other

    def __le__(self, other):
        if isinstance(other, Emotion):
            return self.emotional_flow <= other.emotional_flow
        return self.emotional_flow <= other

    def __eq__(self, other):
        if isinstance(other, Emotion):
            if other._dimension == self.dimension:
                return self.emotional_flow == other.emotional_flow
            return False
        return self.name == other

    def __ne__(self, other):
        if isinstance(other, Emotion):
            if other._dimension == self.dimension:
                return self.emotional_flow != other.emotional_flow
            return True
        return self.name != other

    def __gt__(self, other):
        if isinstance(other, Emotion):
            return self.emotional_flow > other.emotional_flow
        return self.emotional_flow > other

    def __ge__(self, other):
        if isinstance(other, Emotion):
            return self.emotional_flow >= other.emotional_flow
        return self.emotional_flow >= other

    def __contains__(self, item):
        if isinstance(item, str):
            item = self.string_to_emotion(item)
        if isinstance(item, Emotion):
            return item in self.components
        if isinstance(item, EmotionalDimension):
            return self.dimension == item
        return NotImplemented


class CompositeDimension(object):
    def __init__(self):
        self.dimensions = []

    @property
    def name(self):
        name = "/"
        for d in self.dimensions:
            name += d.axis + "/"
        return name[1:-1]

    @property
    def intense_emotion(self):
        if self.name == "attention/sensitivity" or self.name == "sensitivity/attention":
            return COMPOSITE_EMOTIONS["aggressiveness"]
        if self.name == "aptitude/sensitivity" or self.name ==  "sensitivity/aptitude":
            return COMPOSITE_EMOTIONS["rivalry"]
        if self.name == "pleasantness/attention" or self.name == "attention/pleasantness":
            return COMPOSITE_EMOTIONS["optimism"]
        if self.name == "pleasantness/aptitude" or self.name == "aptitude/pleasantness":
            return COMPOSITE_EMOTIONS["love"]
        # TODO science this
        return None

    @property
    def intense_opposite(self):
        if self.name == "attention/sensitivity" or self.name == "sensitivity/attention":
            return COMPOSITE_EMOTIONS["awe"]
        if self.name == "aptitude/sensitivity" or self.name == "sensitivity/aptitude":
            return COMPOSITE_EMOTIONS["coercion"]
        if self.name == "pleasantness/attention" or self.name == "attention/pleasantness":
            return COMPOSITE_EMOTIONS["disapproval"]
        if self.name == "pleasantness/aptitude" or self.name == "aptitude/pleasantness":
            return COMPOSITE_EMOTIONS["remorse"]
        # TODO science this
        return None

    @property
    def mild_emotion(self):
        if self.name == "attention/sensitivity" or self.name == "sensitivity/attention":
            return COMPOSITE_EMOTIONS["anxiety"]
        if self.name == "aptitude/sensitivity" or self.name == "sensitivity/aptitude":
            return COMPOSITE_EMOTIONS["submission"]
        if self.name == "pleasantness/attention" or self.name == "attention/pleasantness":
            return COMPOSITE_EMOTIONS["frustration"]
        if self.name == "pleasantness/aptitude" or self.name == "aptitude/pleasantness":
            return COMPOSITE_EMOTIONS["envy"]
        # TODO science this
        return None

    @property
    def mild_opposite(self):
        if self.name == "attention/sensitivity" or self.name == "sensitivity/attention":
            return COMPOSITE_EMOTIONS["rejection"]
        if self.name == "aptitude/sensitivity" or self.name == "sensitivity/aptitude":
            return COMPOSITE_EMOTIONS["contempt"]
        if self.name == "pleasantness/attention" or self.name == "attention/pleasantness":
            return COMPOSITE_EMOTIONS["frivolity"]
        if self.name == "pleasantness/aptitude" or self.name == "aptitude/pleasantness":
            return COMPOSITE_EMOTIONS["gloat"]
        # TODO science this
        return None

    @property
    def basic_emotion(self):
        # TODO science this
        return None

    @property
    def basic_opposite(self):
        # TODO science this
        return None

    def __repr__(self):
        return "CompositeDimensionObject:" + self.name

    def __add__(self, other):
        if isinstance(other, EmotionalDimension):
            d = copy(self)
            d.dimensions.append(other)
            return d
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, EmotionalDimension):
            d = copy(self)
            if other in d.dimensions:
                d.dimensions.remove(other)
            else:
                return None
            if len(d.dimensions) == 1:
                return d.dimensions[0]
            return d
        return NotImplemented

    def __contains__(self, item):
        if isinstance(item, Neutrality):
            return True
        if isinstance(item, Emotion):
            for d in self.dimensions:
                if d in item:
                    return True
            return False
        if isinstance(item, EmotionalDimension):
            if item in self.dimensions:
                return True

        if isinstance(item, Feeling):
            for d in item.dimensions:
                if d not in self.dimensions:
                    return False
            return True

        return False


def _get_composites():
    bucket = {}
    from emotion_data.emotions import EMOTIONS
    for emo in COMPOSITE_EMOTIONS_NAMES:
        c = CompositeEmotion(emo)
        for e in COMPOSITE_EMOTIONS_NAMES[emo]:
            e = EMOTIONS[e]
            c.components.append(e)
        bucket[emo] = c
    return bucket


COMPOSITE_EMOTIONS = _get_composites()

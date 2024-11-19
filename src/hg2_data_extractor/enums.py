from enum import Enum


class Server(Enum):
    JP = "JP"
    CN = "CN"


class Preset(Enum):
    ITEMS = "items"
    STORY = "story"


class ItemData(Enum):
    WEAPON = "WeaponDataV3"
    COSTUME = "CostumeDataV2"
    BADGE = "PassiveSkillDataV3"
    SKILL = "SpecialAttributeDataV2"
    PET = "PetData"
    PET_SKILL = "PetSkillData"


class StoryData(Enum):
    PLAYBACK = "PlayBackStoryData"
    PLAYBACK_TITLE = "PlayBackStoryTitleData"
    EXT = "StoryExtData"
    FIGUE = "StoryFigueSettingData"
    MAIN = "StoryMainData"
    SUB = "StorySubData"
    CHOICE = "StoryChoiceData"
    PARTNER = "PartnerStoryHeadData"
    PARTNER_POSTER = "PartnerPosterData"
    STORY = "StoryDataV2"
    LIBRARY = "LibraryData"
    LIBRARY_KEYWORD = "LibraryKeyWordData"
    DLC = "DLCStory"


PRESETS: dict[Preset, list[str]] = {
    Preset.ITEMS: [item.value for item in ItemData],
    Preset.STORY: [story.value for story in StoryData],
}

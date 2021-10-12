# Constanta declaration
MANGA_SOURCE_MANGADEX = 'mangadex'
MANGA_SOURCE_SELECTION = [
    (MANGA_SOURCE_MANGADEX, 'Mangadex'),
]

ATTRIBUTE_TYPE_TAG = 'tag'
ATTRIBUTE_TYPE_TITTLE = 'title'
ATTRIBUTE_TYPE_DESCRIPTION = 'desc'
ATTRIBUTES_TYPE_SELECTION = [
    (ATTRIBUTE_TYPE_TAG, 'Tag'),
    (ATTRIBUTE_TYPE_TITTLE, 'Title'),
    (ATTRIBUTE_TYPE_DESCRIPTION, 'Description'),
]

STATE_HIATUS = 'hiatus'
STATE_ONGOING = 'ongoing'
STATE_COMPLETED = 'completed'
STATE_CANCELLED = 'cancelled'
MANGA_STATES_SELECTION = [
    (STATE_HIATUS, 'Hiatus'),
    (STATE_ONGOING, 'Ongoing'),
    (STATE_COMPLETED, 'Completed'),
    (STATE_CANCELLED, 'Cancelled'),
]

CONTENT_RATING_SAFE = 'safe'
CONTENT_RATING_MATURE = 'mature'
CONTENT_RATING_SELECTION = [
    (CONTENT_RATING_SAFE, 'Safe'),
    (CONTENT_RATING_MATURE, 'Mature'),
]

SOCIAL_MEDIA_TYPE_PIXIV = 'pixiv'
SOCIAL_MEDIA_TYPE_YOUTUBE = 'youtube'
SOCIAL_MEDIA_TYPE_WEBSITE = 'website'
SOCIAL_MEDIA_TYPE_TWITTER = 'twitter'
SOCIAL_MEDIA_TYPE_MELONBOOK = 'melonbook'
SOCIAL_MEDIA_TYPE_NICOVIDEO = 'nicovideo'
SOCIAL_MEDIA_TYPE_FANTIA = 'fantia'
SOCIAL_MEDIA_TYPE_TUMBLR = 'tumblr'
SOCIAL_MEDIA_TYPE_FANBOX = 'fanbox'
SOCIAL_MEDIA_TYPE_BOOTH = 'booth'
SOCIAL_MEDIA_TYPE_SKEB = 'skeb'
SOCIAL_MEDIAL_TYPE_SELECTION = [
    (SOCIAL_MEDIA_TYPE_PIXIV, 'Pixiv'),
    (SOCIAL_MEDIA_TYPE_YOUTUBE, 'Youtube'),
    (SOCIAL_MEDIA_TYPE_WEBSITE, 'Website'),
    (SOCIAL_MEDIA_TYPE_TWITTER, 'Twitter'),
    (SOCIAL_MEDIA_TYPE_MELONBOOK, 'Melon Book'),
    (SOCIAL_MEDIA_TYPE_NICOVIDEO, 'Nico Video'),
    (SOCIAL_MEDIA_TYPE_FANTIA, 'Fantia'),
    (SOCIAL_MEDIA_TYPE_TUMBLR, 'Tumblr'),
    (SOCIAL_MEDIA_TYPE_FANBOX, 'Fanbox'),
    (SOCIAL_MEDIA_TYPE_BOOTH, 'Booth'),
    (SOCIAL_MEDIA_TYPE_SKEB, 'Skeb'),
]

QUALITY_LOW = 'low'
QUALITY_HIGH = 'high'
QUALITY_MEDIUM = 'medium'
QUALITY_SELECTION = [
    (QUALITY_LOW, 'Low'),
    (QUALITY_HIGH, 'High'),
    (QUALITY_MEDIUM, 'Medium'),
]
from __future__ import absolute_import, annotations

import re
from numbers import Number
from typing import List, Optional

from wenet.model.common import Gender, Date, UserLanguage
from wenet.model.norm import Norm
from babel.core import Locale


class WeNetUserProfile:

    def __init__(self,
                 name: UserName,
                 date_of_birth: Date,
                 gender: Optional[Gender],
                 email: Optional[str],
                 phone_number: Optional[str],
                 locale: Optional[str],
                 avatar: Optional[str],
                 nationality: Optional[str],
                 languages: List[UserLanguage],
                 occupation: Optional[str],
                 creation_ts: Optional[Number],
                 last_update_ts: Optional[Number],
                 profile_id: str,
                 norms: List[Norm],
                 planned_activities: list,
                 relevant_locations: list,
                 relationships: list,
                 social_practices: list,
                 personal_behaviours: list
                 ):
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.phone_number = phone_number
        self.locale = locale
        self.avatar = avatar
        self.nationality = nationality
        self.languages = languages
        self.occupation = occupation
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.profile_id = profile_id
        self.norms = norms
        self.planned_activities = planned_activities
        self.relevant_locations = relevant_locations
        self.relationships = relationships
        self.social_practices = social_practices
        self.personal_behaviours = personal_behaviours

        if not isinstance(name, UserName):
            raise TypeError("Name should be a UserName object")
        if not isinstance(date_of_birth, Date):
            raise TypeError("Date of birth should be a Date")
        if gender:
            if not isinstance(gender, Gender):
                raise TypeError("Gender should be a Gender object")
        if email:
            if not isinstance(email, str):
                raise TypeError("Email should be a string")
            if not self.is_valid_mail(email):
                raise ValueError("[%s] is not a valid email" % email)
        if phone_number:
            if not isinstance(phone_number, str):
                raise TypeError("Phone number should be a string")
        if locale:
            if not isinstance(locale, str):
                raise TypeError("Locale should be a string")
            if not self.is_valid_locale(locale):
                raise ValueError("[%s] is not a valid Locale" % locale)
        if avatar:
            if not isinstance(avatar, str):
                raise TypeError("Avatar should be a string")
        if nationality:
            if not isinstance(nationality, str):
                raise TypeError("Nationality should be a string")

        if not isinstance(languages, list):
            raise TypeError("Languages should be list of UserLanguage")
        else:
            for language in languages:
                if not isinstance(language, UserLanguage):
                    raise TypeError("Languages should be list of UserLanguage")
        if occupation:
            if not isinstance(occupation, str):
                raise TypeError("Occupation should be a string")

        if creation_ts:
            if not isinstance(creation_ts, Number):
                raise TypeError("CreationTs should be a string")
        if last_update_ts:
            if not isinstance(last_update_ts, Number):
                raise TypeError("LastUpdateTs should be a string")

        if not isinstance(profile_id, str):
            raise TypeError("Profile id should be a string")

        if not isinstance(norms, list):
            raise TypeError("Norms should be a list of norms")
        else:
            for norm in norms:
                if not isinstance(norm, Norm):
                    raise TypeError("Norms should be a list of norms")

        if not isinstance(planned_activities, list):
            raise TypeError("PlannedActivities should be a list")
        if not isinstance(relevant_locations, list):
            raise TypeError("RelevantLocations should be a list")
        if not isinstance(relationships, list):
            raise TypeError("Relationship should be a list")
        if not isinstance(social_practices, list):
            raise TypeError("SocialPractices should be a list")
        if not isinstance(personal_behaviours, list):
            raise TypeError("personalBehaviors should be a list")

    def to_repr(self) -> dict:
        return {
            "name": self.name.to_repr(),
            "dateOfBirth": self.date_of_birth.to_repr(),
            "gender": self.gender.value if self.gender else None,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "locale": self.locale,
            "avatar": self.avatar,
            "nationality": self.nationality,
            "languages": list(x.to_repr() for x in self.languages),
            "occupation": self.occupation,
            "_creationTs": self.creation_ts,
            "_lastUpdateTs": self.last_update_ts,
            "id": self.profile_id,
            "norms": list(x.to_repr() for x in self.norms),
            "plannedActivities": self.planned_activities,
            "relevantLocations": self.relevant_locations,
            "relationships": self.relationships,
            "socialPractices": self.social_practices,
            "personalBehaviors": self.personal_behaviours
        }

    @staticmethod
    def from_repr(raw_data: dict) -> WeNetUserProfile:
        return WeNetUserProfile(
            name=UserName.from_repr(raw_data["name"]),
            date_of_birth=Date.from_repr(raw_data["dateOfBirth"]),
            gender=Gender(raw_data["gender"]) if raw_data.get("gender", None) else None,
            email=raw_data.get("email", None),
            phone_number=raw_data.get("phoneNumber", None),
            locale=raw_data.get("locale", None),
            avatar=raw_data.get("avatar", None),
            nationality=raw_data.get("nationality", None),
            languages=list(UserLanguage.from_repr(x) for x in raw_data["languages"]),
            occupation=raw_data.get("occupation", None),
            creation_ts=raw_data.get("_creationTs", None),
            last_update_ts=raw_data.get("_lastUpdateTs", None),
            profile_id=raw_data["id"],
            norms=list(Norm.from_repr(x) for x in raw_data["norms"]),
            planned_activities=raw_data["plannedActivities"],
            relevant_locations=raw_data["relevantLocations"],
            relationships=raw_data["relationships"],
            social_practices=raw_data["socialPractices"],
            personal_behaviours=raw_data["personalBehaviors"]
        )

    @staticmethod
    def is_valid_mail(mail: str):
        reg_exp = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w+)+$"
        return re.search(reg_exp, mail)

    @staticmethod
    def is_valid_locale(locale: str) -> bool:
        try:
            Locale.parse(locale)
            return True
        except ValueError:
            return False

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, WeNetUserProfile):
            return False
        return self.name == o.name and self.date_of_birth == o.date_of_birth and self.gender == o.gender and self.email == o.email \
            and self.phone_number == o.phone_number and self.locale == o.locale and self.avatar == o.avatar and self.nationality == o.nationality \
            and self.languages == o.languages and self.occupation == o.occupation and self.creation_ts == o.creation_ts and self.last_update_ts == o.last_update_ts \
            and self.profile_id == o.profile_id and self.norms == o.norms and self.planned_activities == o.planned_activities and self.relevant_locations == o.relationships \
            and self.relationships == o.relationships and self.social_practices == o.social_practices and self.personal_behaviours == o.personal_behaviours


class UserName:

    def __init__(self, first: Optional[str], middle: Optional[str], last: Optional[str], prefix: Optional[str], suffix: Optional[str]):
        self.first = first
        self.middle = middle
        self.last = last
        self.prefix = prefix
        self.suffix = suffix

        if first:
            if not isinstance(first, str):
                raise TypeError("First should be a string")
        if middle:
            if not isinstance(middle, str):
                raise TypeError("Middle should be a string")
        if last:
            if not isinstance(last, str):
                raise TypeError("Last should be a string")
        if prefix:
            if not isinstance(prefix, str):
                raise TypeError("Prefix should be a string")
        if suffix:
            if not isinstance(suffix, str):
                raise TypeError("Suffix should be a string")

    def to_repr(self) -> dict:
        return {
            "first": self.first,
            "middle": self.middle,
            "last": self.last,
            "prefix": self.prefix,
            "suffix": self.suffix
        }

    @staticmethod
    def from_repr(raw_data: dict) -> UserName:
        return UserName(
            first=raw_data.get("first", None),
            middle=raw_data.get("middle", None),
            last=raw_data.get("last", None),
            prefix=raw_data.get("prefix", None),
            suffix=raw_data.get("suffix", None)
        )

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, UserName):
            return False
        return self.first == o.first and self.middle == o.middle and self.last == o.last and self.prefix == o.prefix and self.suffix == o.suffix

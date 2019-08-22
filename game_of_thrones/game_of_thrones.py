from iconservice import *

TAG = 'GameOfThrones'

class GameOfThrones(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._family_to_alliance = DictDB('family_to_alliance', db, value_type=str, depth=1)
        self._alliances = ArrayDB("alliances", db, value_type=str)
        self._families = ArrayDB("families", db, value_type=str)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()


    @external
    def createAlliance(self, alliance: str) -> None:
        if self.existsAlliance(alliance) == True:
            revert("alliance already exists")
        self._alliances.put(alliance)

    @external(readonly=True)
    def getFamiliesOfAlliance(self, alliance: str) -> list:
        if self.existsAlliance(alliance) == False:
            revert("alliance doesn't exist yet")
        familiesOfAlliance = []
        for family in self._families:
            if self._family_to_alliance[family] == alliance:
                familiesOfAlliance.append(family)
        return familiesOfAlliance

    @external
    def createFamilyAndAttachToAlliance(self, family: str, alliance: str) -> None:
        if self.existsAlliance(alliance) == False:
            revert("alliance doesn't exist yet")
        elif self.existsFamily(family) == True:
            revert("family already exists")
        self._families.put(family)
        self._family_to_alliance[family] = alliance

    @external
    def transferFamily(self, family: str, currentAlliance: str, newAlliance: str) -> None:
        if self.existsAlliance(currentAlliance) == False:
            revert("currentAlliance doesn't exist yet")
        elif self.existsAlliance(newAlliance) == False:
            revert("newAlliance doesn't exist yet")
        elif self.existsFamily(family) == False:
            revert("family doesn't exist yet")
        elif self._family_to_alliance[family] != currentAlliance:
            revert("family isn't part of currentAlliance")
        self._family_to_alliance[family] = newAlliance

    @external(readonly=True)
    def existsAlliance(self, alliance: str) -> bool:
        if alliance in self._alliances:
            return True
        else:
            return False

    @external(readonly=True)
    def existsFamily(self, family: str) -> bool:
        if family in self._families:
            return True
        else:
            return False

    @external(readonly=True)
    def getAllianceOfFamily(self, family: str) -> str:
        if self.existsFamily(family) == False:
            revert("family doesn't exist yet")
        return self._family_to_alliance[family]

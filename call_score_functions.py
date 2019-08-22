import time
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
icon_service = IconService(HTTPProvider("http://localhost:9000", 3))
from iconsdk.wallet.wallet import KeyWallet

from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.call_builder import CallBuilder

scoreAddress = "PUT YOUR_SCORE_ADDRESS HERE"

wallet = KeyWallet.load("./keystore_test1", "test1_Account")


def readTransaction(method: str, params: []) -> {}:
    call = CallBuilder().from_(wallet.get_address())\
                    .to(scoreAddress)\
                    .method(method)\
                    .params(params)\
                    .build()
    result =  icon_service.call(call)
    print(result)
    return result

def writeTransaction(method: str, params: []) -> {}:
    transaction = CallTransactionBuilder()\
                  .from_(wallet.get_address())\
                  .to(scoreAddress)\
                  .step_limit(100000000)\
                  .nid(3)\
                  .nonce(100)\
                  .method(method)\
                  .params(params)\
                  .build()
    signed_transaction = SignedTransaction(transaction, wallet)
    tx_hash = icon_service.send_transaction(signed_transaction)
    time.sleep(10)
    result = icon_service.get_transaction_result(tx_hash)
    print(result)
    return result


allianceKhaleesi = "Khaleesi"
allianceCercei = "Cercei"

familyTargaryen = "Targaryen"
familyLannister = "Lannister"
familyStark = "Stark"

print("create alliances")
paramsKhaleesi = {"alliance": allianceKhaleesi}
paramsCercei = {"alliance": allianceCercei}

assert readTransaction("existsAlliance", paramsKhaleesi) == '0x0', "alliance exists already?!"
assert readTransaction("existsAlliance", paramsCercei) == '0x0', "alliance exists already?!"
writeTransaction("createAlliance", paramsKhaleesi)
writeTransaction("createAlliance", paramsCercei)

assert readTransaction("existsAlliance", paramsKhaleesi) == '0x1', "alliance doesn't exist?!"
assert readTransaction("existsAlliance", paramsCercei) == '0x1', "alliance doesn't exist?!"



print("create and add families to alliances")
paramsTargaryen = {"family": familyTargaryen}
paramsLannister = {"family": familyLannister}
paramsStark = {"family": familyStark}


assert readTransaction("existsFamily", paramsTargaryen) == '0x0', "family exists already?!"
assert readTransaction("existsFamily", paramsLannister) == '0x0', "family exists already?!"
assert readTransaction("existsFamily", paramsStark) == '0x0', "family exists already?!"

writeTransaction("createFamilyAndAttachToAlliance", {"family": familyTargaryen, "alliance": allianceKhaleesi})
writeTransaction("createFamilyAndAttachToAlliance", {"family": familyLannister, "alliance": allianceCercei})
writeTransaction("createFamilyAndAttachToAlliance", {"family": familyStark, "alliance": allianceKhaleesi})

assert readTransaction("existsFamily", paramsTargaryen) == '0x1', "family doesn't exist?!"
assert readTransaction("existsFamily", paramsLannister) == '0x1', "family doesn't exist?!"
assert readTransaction("existsFamily", paramsStark) == '0x1', "family doesn't exist?!"
assert readTransaction("getAllianceOfFamily", paramsTargaryen) == allianceKhaleesi, "family is part of the wrong alliance"
assert readTransaction("getAllianceOfFamily", paramsLannister) == allianceCercei, "family is part of the wrong alliance"
assert readTransaction("getAllianceOfFamily", paramsStark) == allianceKhaleesi, "family is part of the wrong alliance"


print("transfer families")
writeTransaction("transferFamily", {"family": familyStark, "currentAlliance": allianceKhaleesi, "newAlliance": allianceCercei})
writeTransaction("transferFamily", {"family": familyTargaryen, "currentAlliance": allianceKhaleesi, "newAlliance": allianceCercei})

assert readTransaction("getAllianceOfFamily", paramsStark) == allianceCercei, "family is part of the wrong alliance"
assert readTransaction("getAllianceOfFamily", paramsTargaryen) == allianceCercei, "family is part of the wrong alliance"
assert len(readTransaction("getFamiliesOfAlliance", paramsKhaleesi)) == 0, "alliance of khaleesi should not contain any families"
familiesOfCercei = readTransaction("getFamiliesOfAlliance", paramsCercei)
for family in familiesOfCercei:
    assert family == familyLannister or family == familyTargaryen or family == familyStark, "all families should be in Cercei's alliance"

print("SUCCESS!")
print("EVERYTHING WORKED, WELL DONE ICONIST.")
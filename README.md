# Game of Thrones on ICON 🤴⚔

<div>
  <a href="#">
    <img src="https://img.shields.io/badge/language-Python-brightgreen.svg" alt="Language" />
  </a>
  <a href="https://t.me/block42_crypto">
    <img src="https://img.shields.io/badge/chat-telegram-0088cc.svg" alt="Telegram" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
  </a>
</div>

<br />

Implementation of a simple game of thrones use case on ICON.

We developed our icon game of thrones use case with the help of the icon-tbears docker container.

We coded two files for this use case. In the current `icon-game-of-thrones` folder, the important file is `call_score_functions.py`. 
In this file we made use of ICON's Python SDK, to interact with our game of thrones smart contract, and to test that everything works fine.
Inside the `game_of_thrones` folder, the `game_of_thrones.py` file is the actual smart contract. In Icon smart contracts are called `SCORE`.

The official documentation is very helpful, and should be taken as a reference to understand the code that we wrote (https://www.icondev.io/docs/writing-score).

If you have docker installed and cloned this repo, you're ready to go.
In your terminal type `docker run -it --name local-tbears -p 9000:9000 -v ~/YOUR/PATH/TO/icon-game-of-thrones:/work iconloop/tbears:mainnet`.
This command downloads the tbears image, starts the container and takes your stdin/stdout inside the container.
The `-v` option connects the cloned `icon-game-of-thrones` folder to the `work` folder of the container.
That way, you can conveniently edit files with your favorite editor on the host machine, while enjoying the fully functional development environment of the container.

Once inside the container, hit `ls` to make sure that you can see all files that are inside the `icon-game-of-thrones` folders in this repository and on your host machine respectively.
Then type `tbears deploy game_of_thrones`. This will submit a deploy transaction to deploy our smart contract to the local icon environment. 

You should see something like:

```
Send deploy request successfully.
If you want to check SCORE deployed successfully, execute txresult command
transaction hash: <TX HASH>
```

Copy the address of the transaction hash and use it to call the `tbears txresult` command like this:

```
tbears txresult <TX HASH>
```

This should output you a successful transaction result similar to this:

```
Transaction result: {
    "jsonrpc": "2.0",
    "result": {
        "txHash": "0x2607d54bcf2a766659947fc5877768954102b3836e64d29ee21a788444f15caa",
        "blockHeight": "0x3a",
        "blockHash": "0x168332c72f237dfdc54fe5b3dafe068affba041f1ded8cb97f00e84fd295f42c",
        "txIndex": "0x0",
        "to": "cx0000000000000000000000000000000000000000",
        "scoreAddress": "cx8f97bdfa6ce30b3ab11cb606ac1c54862cbbd36c",
        "stepUsed": "0x2116690",
        "stepPrice": "0x0",
        "cumulativeStepUsed": "0x2116690",
        "eventLogs": [],
        "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "status": "0x1"
    },
    "id": 1
}
```

Now copy the scoreAddress `cx8f97bdfa6ce30b3ab11cb606ac1c54862cbbd36c` from the transaction result, open the `call_score_functions.py` file and replace the content of the scoreAddress variable with the actual hexNumber you just copied.
Finally, in the terminal that is connected to the tbears container, enter `python3 call_score_functions.py` and make sure that it runs through until you see Success!

## Licence

This project is licensed under the MIT license. For more information see LICENSE.md.

```
The MIT License

Copyright (c) 2019 block42 Blockchain Company GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

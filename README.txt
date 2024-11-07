# Airgapped wallet

## Forger - safely create a new random wallet 

```bash
python forger.py
```

### Docker

```bash
docker build -t forger .
docker run -rm forger
```

## Enchanter - get encrypted private key from the mnemonic

```bash
python enchanter.py <your password>
``` 

or 

```bash
cat << EOF | python enchanter.py
<your password>
EOF
```

### Docker

```bash
docker build -t enchanter .
docker run -rm enchanter <your password>
```

or

```bash
docker run -i -rm enchanter
<your password><EOF>
```

## Address weaver - get the address from the mnoemonic

```bash
cat << EOF | python address_weaver.py
<your mnemonic>
EOF
```

or 

```bash
python address_weaver.py <your mnemonic>
```

### Docker

```bash
docker build -t address_weaver .
docker run -rm address_weaver <your mnemonic>
```

or 

```bash
docker run -i -rm address_weaver
<your mnemonic><EOF>
```

## Pipenv

Initialize the virtual environment with pipenv

```bash
pipenv shell
```

## References

https://docs.ethers.org/v6/api/wordlists/

https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

https://github.com/trezor/python-mnemonic

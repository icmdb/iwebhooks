# iwebhooks

Webhooks

## Quick Start

### 1. Start directly:

```bash
pip install -r requirements.txt

python app.py
```

### 2. Start by docker-compose

```bash
docker-compose up -d iwebhook
```

### 3. Deploy in kubernetes by helm

```bash
helm install iwebhook 
```

## Test

```bash
cp client.env.example client.env

# Change config in client.env
source client.env

python client.py
```

## Alicloud Container Registry Service

* [islack](islack/README.md)
* [idingtalk](idingtalk/README.md)
* [ibearychat](ibearychat/README.md)

### 1. Deploy Webhooks

### 2. Setting IM

* 2.1 Create a channel for slack or a group for bearychat/dingtalk.
* 2.2 Setting incoming robot.

### 3. Create Image Registry on alicloud

### 4. Setting webhooks

### 5. Push demo



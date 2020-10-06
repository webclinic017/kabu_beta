# kabu_beta
張が独自開発した株情報取得機能です。

## ローカル開発環境立上げ情報（with docker）


### 1. githubからソースコードをclone

``` shell
$ git clone https://github.com/zhanglizhu-tokyo/kabu_beta/
```

### 2. docker compose containerを立上げる。
下記のコマンドを使ってローカルにdocker containerを立上げることができます。

``` shell
$ docker-compose build
  ...

$ docker-compose up -d

Recreating kabu_beta_db_1 ... done
Creating python_web       ... 
Creating python_web       ... done
起動失敗の場合,以下を試してください
$ docker-compose up --force-recreate
  ...

```

### 3. ローカル環境に接続する方法
ローカルのhostsファイルに下記の１行を追加

```shell
127.0.0.1	kabu.com
```



### 5. ローカル環境のwebへ接続する方法
開発環境のserverに接続する方法は下記にの通り

```shell
docker-compose exec web bash


```
### 5. ローカル環境のDBへ接続する方法
開発環境のpostgreSQLに接続する方法は下記にの通り
```
docker-compose exec db bash

```

### Front
気に入り銘柄
```
http://kabu.com:9090/front/favoritelist/
```

銘柄詳細
```
http://kabu.com:9090/front/companyinfo/1811
```



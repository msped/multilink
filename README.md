# Multi Link API

Multi Link is a Link Tree clone in React and Django Rest Framework. This repository is just for the API.

## Technologies 

-   [Django](https://www.djangoproject.com/)
-   [Django Rest Framework](https://www.django-rest-framework.org/)
-   [Djoser](https://github.com/sunscrapers/djoser)
-   [Coverage](https://coverage.readthedocs.io/en/6.5.0/)
-   [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)
-   [Django Rest Framework Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
-   [Pillow](https://python-pillow.org/)
-   [Python DotEnv](https://github.com/theskumar/python-dotenv)

## Endpoints

### Auth

#### Obtain Token (Login)

```/api/auth/jwt/token/ POST```

```
{
    'username': string, 
    'password': string
}
```

Returns `access`, `refresh`, and `username`.

#### Refresh Token

```/api/auth/jwt/refresh/ POST```

```
    {
        'refresh': string
    }
```

#### Blacklist Token (Logout)

```/api/auth/jwt/blacklist/ POST```

```
    {
        'refresh': string
    }
```

#### Register Account

```/api/auth/users/ POST```

```
{
    'username': string, 
    'password': string,
    'password': string,
    're_password': string
}
```

#### Logout (Blacklist Token)
```/api/auth/jwt/blacklist/ POST```

```
{
    'refresh': string
}
```
Takes the refresh token as the request data.

#### Change Password
```/api/auth/change-password/ POST```

```
{
    'old_password': string,
    'new_password': string,
    'new_password2': string
}
```

### Links

#### Create Link
```/api/links/ POST```

```
{
    'network': int(id),
    'link': string(URL),
    'nsfw': boolean
}
```

`nsfw` defaults to `False` and will only need to be added if it is `True`.

#### Get Networks
```/api/links/networks/ GET```

#### Update, Destroy Link
```/api/links/:pk/ PUT PATCH DELETE```

```
{
    'network': int(id),
    'link': string,
    'nsfw': boolean
}
```

#### Profile
```/api/links/:username/ GET```

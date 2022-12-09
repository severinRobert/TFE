# TFE
## Description
The goal is to create a modular web application for customer to customer sale.

## Install
The application can be install via a docker or a bash script.

There are different options :
* DB is optional
* Backend API is optional
* Frontend is mandatory
* Authentification is optional

Some pre-configurations are available for books oriented C2C.

## Technologies
### React ou vue


## Frontend
### Pages
* Home
  * description : introduction to the site.
  * route API : None.
  * security : low.
* Offers
  * description : list of offers of the users.
  * route API : `[GET]/offers`.
  * security : middle.
* Demands
  * description : list of demands of the users.
  * route API : `[GET]/demands`.
  * security : middle.
* Form
  * description : form to let the user add his offer/demand.
  * route API : `[POST]/offer`, `[POST]/demand`.
  * security : high.
* Profile
  * description : profile of the user, where he can modify his data.
  * route API : `[GET]/user`, `[POST]/user/name`.
  * security : middle.
* Settings
  * description : settings about the platform.
  * route API : `[GET]/settings`, `[POST]/settings/security/{user}`.
  * security : high.
* Statistics
  * description : see statistics about the platform.
  * route API : `[GET]/statistics`.
  * security : high.

## Backend
### Routes API
* Offers
  * GET
    * /offers
  * POST
    * /offer
* Demands
  * GET
    * /demands
  * POST
    * /demand
* Users
  * GET
    * /users
    * /users/{id}
  * POST
    * /users/{id}
      * {name: {name}}
* Settings
  * GET
    * /settings
  * POST
    * /settings/security/{user}
* Statistics
  * GET
    * /statistics

## Security
Groups of users by default :
* visitor : lower access, visitors of the site.
  * Frontend pages : Home.
  * Backend routes : None.
* user : middle access, authentified users.
  * Frontend pages : Home, Offers, Demands, Form, Profile.
  * Backend routes : TODO.
* admin : high access, administrator of the system.
  * Frontend pages : Home, Offers, Demands, Settings, Statistics.
  * Backend routes : TODO.

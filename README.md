Wazo dird plugin Odoo
======================

## Info

This plugin gets contacts from Odoo v7 or v8. (only tested with v8 community edition)

Works only with **Wazo >= 20.11**

## How to install

### CLI

    apt-get install wazo-plugind-cli
    wazo-plugind-cli -c "install git https://github.com/sboily/wazo-dird-plugin-backend-odoo"
    
### Interface

Go to our new web interface on plugins link.
In git tab add:

    https://github.com/sboily/wazo-dird-plugin-backend-odoo
    
Then click to install the plugin.

## How to configure

Use API or Wazo-platform UI.


**Optional**: On the Odoo side, you need to install the *base_phone* module, which is a module of the [Odoo Community Association](https://odoo-community.org/) available on the [connector-telephony](https://github.com/OCA/connector-telephony) github project. When you install this module, a wizard will propose you to reformat the phone numbers in E.164 format ; you should follow the instructions of the wizard.

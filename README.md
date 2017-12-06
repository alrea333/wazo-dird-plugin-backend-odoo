Wazo dird plugin Odoo
======================

## Info

This plugin gets contacts from Odoo v7 or v8. (only tested with v8 community edition)

## How to use

Optional: On the Odoo side, you need to install the *base_phone* module, which is a module of the [Odoo Community Association](https://odoo-community.org/) available on the [connector-telephony](https://github.com/OCA/connector-telephony) github project. When you install this module, a wizard will propose you to reformat the phone numbers in E.164 format ; you should follow the instructions of the wizard.

## How to install

### CLI

    apt-get install wazo-plugind-cli
    wazo-plugind-cli -c "install git https://github.com/sboily/wazo-dird-plugin-backend-odoo"
    
### Interface

Go to our new web interface on plugins link. In git tab add "https://github.com/sboily/wazo-dird-plugin-backend-odoo" and clic to install.

## How to configure

On the Wazo side, in the config file */etc/xivo-dird/conf.d/odoo.yml*, configure the odoo information for the plugin:

    enabled_plugins:
      backends:
        odoo : true
    
    services:
      lookup:
        default:
          timeout: 10
          sources:
            odoo: true
    
    sources:
      odoo:
        type: odoo
        name: odoo
        odoo_config:
          server: odoo
          port: 8069
          database: prod
          userid: 1
          password: secret
        format_columns:
          name: '{firstname} {lastname}'
          display_name: '{firstname} {lastname}'
          phone_mobile: '{mobile}'
          reverse: '{firstname} {lastname}'
          
The plugin is activated by default.

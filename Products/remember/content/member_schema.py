from Products.CMFPlone import utils as plone_utils
from Products.Archetypes import public as atapi
from Products.Archetypes.utils import shasattr

from Products.remember.permissions import VIEW_PUBLIC_PERMISSION, \
     EDIT_ID_PERMISSION, VIEW_OTHER_PERMISSION, EDIT_PROPERTIES_PERMISSION, \
     VIEW_SECURITY_PERMISSION, EDIT_PASSWORD_PERMISSION, \
     EDIT_SECURITY_PERMISSION, MAIL_PASSWORD_PERMISSION, ADD_PERMISSION, \
     VIEW_PERMISSION, REGISTER_PERMISSION


##############
## ID_SCHEMA
##############
id_schema = atapi.Schema((
    atapi.StringField('id',
                       required=1,
                       accessor='getId',
                       mutator='setId',
                       mode='rw',
                       read_permission=VIEW_PUBLIC_PERMISSION,
                       write_permission=EDIT_ID_PERMISSION,
                       default=None,
                       index=('membrane_tool/ZCTextIndex,lexicon_id=member_lexicon,index_type=Cosine Measure|TextIndex:brains',
                              'FieldIndex:brains'),
                 widget=atapi.IdWidget(label='User name',
                                  label_msgid='label_user_name',
                                  size=10,
                                  maxlength=25,
                                  description="Enter a user name, usually something like "
                                  "'jsmith'. No spaces or special characters. User "
                                  "names and passwords are case sensitive, make sure "
                                  "the capslock key is not enabled. This is the name "
                                  "used to log in.",
                                  description_msgid='help_user_name_creation_casesensitive',
                                  i18n_domain='plone',
                                  display_autogenerated=0,
                                  macro='memid',
                                  ),
                 regfield=1,  ### this field is part of the registration form
                 user_property=True,
                 ),

    atapi.ComputedField('title',
                         searchable=1,
                         expression='context.fileAs() or context.getId()',
                         accessor='Title',
                         widget=atapi.ComputedWidget(label_msgid="label_title",
                                                      i18n_domain="plone"),
                 user_property=True,
                 ),
    ))


#################
## CONTACT_SCHEMA
#################
contact_schema = atapi.Schema((
    atapi.StringField('fullname',
                default='',
                accessor='getFullname',
                mutator='setFullname',
                mode='rw',
                read_permission=VIEW_PUBLIC_PERMISSION,
                write_permission=EDIT_PROPERTIES_PERMISSION,
                index=('membrane_tool/ZCTextIndex,lexicon_id=member_lexicon,index_type=Cosine Measure|TextIndex:brains',
                       'ZCTextIndex|TextIndex:brains'),
                widget=atapi.StringWidget(
                    label='Full name',
                    label_msgid='label_full_name',
                    description="Enter full name, eg. John Smith.",
                    description_msgid='help_full_name_creation',
                    i18n_domain='plone',
                    ),
                regfield=1,
                user_property=True,
                ),

    atapi.StringField('email',
                required=1,
                accessor='getEmail',
                mutator='setEmail',
                mode='rw',
                read_permission=VIEW_PUBLIC_PERMISSION,
                write_permission=EDIT_PROPERTIES_PERMISSION,
                validators=('isEmail',),
                index=('membrane_tool/ZCTextIndex,lexicon_id=member_lexicon,index_type=Cosine Measure|TextIndex:brains',
                       'ZCTextIndex|TextIndex:brains'),
                widget=atapi.StringWidget(
                    label='E-mail',
                    label_msgid='label_email',
                    description="Enter an email address. This is necessary "
                        "in case the password is lost. We respect your privacy "
                        "and will not give the address away to any third "
                        "parties or expose it anywhere.",
                    description_msgid='help_email_creation',
                    i18n_domain='plone',
                    ),
                regfield=1,
                user_property=True,
                ),
    ))

###############
## PLONE_SCHEMA
###############
plone_schema = atapi.Schema((
    atapi.StringField('wysiwyg_editor',
                mode='rw',
                read_permission=VIEW_OTHER_PERMISSION,
                write_permission=EDIT_PROPERTIES_PERMISSION,
                vocabulary='editors',
                enforceVocabulary=1,
                widget=atapi.SelectionWidget(
                    format='select',
                    label='Content editor',
                    label_msgid='label_content_editor',
                    description="Select the editor that you would like to use "
                        "for editing content more easily. Content editors "
                        "often have specific browser requirements.",
                    description_msgid='help_content_editor',
                    i18n_domain='plone',
                    ),
                user_property=True,
                ),

    atapi.StringField('portal_skin',
                mode='rw',
                default=None,
                read_permission=VIEW_OTHER_PERMISSION,
                write_permission=EDIT_PROPERTIES_PERMISSION,
                accessor='getPortalSkin',
                vocabulary='available_skins',
                widget=atapi.SelectionWidget(
                    format='flex',
                    label='Look',
                    label_msgid='label_look',
                    description="Appearance of the site.",
                    description_msgid='help_look',
                    i18n_domain='plone',
                    condition="portal/portal_skins/allow_any",
                    ),
                user_property=True,
                ),

    atapi.ImageField('portrait',
               mode='rw',
               accessor='getPortrait',
               mutator='setPortrait',
               max_size=(150,150),
               read_permission=VIEW_PUBLIC_PERMISSION,
               write_permission=EDIT_PROPERTIES_PERMISSION,
               required=0,
               widget=atapi.ImageWidget(
                   label='Portrait',
                   label_msgid='label_portrait',
                   description="To add or change the portrait: click the "
                       "\"Browse\" button; select a picture of yourself. "
                       "Recommended image size is 75 pixels wide by 100 "
                       "pixels tall.",
                   description_msgid='help_portrait',
                   i18n_domain='plone',
                   ),
               user_property=True,
               ),

    atapi.BooleanField('visible_ids',
                default=1,
                mode='rw',
                accessor='getVisible_ids',
                mutator='setVisible_ids',
                read_permission=VIEW_OTHER_PERMISSION,
                write_permission=EDIT_PROPERTIES_PERMISSION,
                widget=atapi.BooleanWidget(
                    label='Display names',
                    label_msgid='label_edit_short_names',
                    description="Determines if Short Names (also known as "
                        "IDs) are changable when editing items. If Short "
                        "Names are not displayed, they will be generated "
                        "automatically.",
                    description_msgid='help_display_names',
                    visible={'edit': 'invisible',
                             'view': 'invisible'},
                    i18n_domain='plone',
                    ),
                user_property=True,
                ),

    atapi.StringField('home_page',
                      mode='rw',
                      read_permission=VIEW_PUBLIC_PERMISSION,
                      write_permission=EDIT_PROPERTIES_PERMISSION,
                      widget=atapi.StringWidget(
                              label='Home Page',
                              label_msgid='label_home_page',
                              description="Member home page.",
                              description_msgid='help_home_page',
                              i18n_domain='plone',
                              visible={'view':'invisible', 'edit':'invisible'},
                              ),
                      user_property=True,
                      ),

    atapi.StringField('location',
                      mode='rw',
                      read_permission=VIEW_PUBLIC_PERMISSION,
                      write_permission=EDIT_PROPERTIES_PERMISSION,
                      widget=atapi.StringWidget(
                              label='Location',
                              label_msgid='label_location',
                              description="Your location - either city and country - or in a company setting, where your office is located.",
                              description_msgid='help_location',
                              i18n_domain='plone',
                              ),
                      user_property=True,
                      ),

    atapi.StringField('language',
                      accessor='Language',
                      mode='rw',
                      read_permission=VIEW_PUBLIC_PERMISSION,
                      write_permission=EDIT_PROPERTIES_PERMISSION,
                      vocabulary='getSiteLanguages',
                      widget=atapi.SelectionWidget(
                              label='Language',
                              label_msgid='label_language',
                              description="Your preferred language.",
                              description_msgid='help_language',
                              i18n_domain='plone',
                              ),
                      user_property=True,
                      ),

    atapi.TextField('description',
                    default='',
                    searchable=1,
                    accessor="Description",
                    widget=atapi.TextAreaWidget(
                            label='Biography',
                            label_msgid='label_biography',
                            description='A short overview of who you are and what you do. Will be displayed on the your author page, linked from the items you create.',
                            description_msgid='help_biography',
                            i18n_domain='plone',
                            ),
                    user_property=True,
                    ),
    ))

##################
## SECURITY_SCHEMA
##################
security_schema = atapi.Schema((
    atapi.StringField('password',
                mutator='_setPassword',
                accessor='getPassword',
                mode='rw',
                write_permission=EDIT_PASSWORD_PERMISSION,
                widget=atapi.PasswordWidget(
                    label='Password',
                    label_msgid='label_password',
                    description="Minimum 5 characters",
                    visible = {'view' : 'invisible' },
                    description_msgid='help_password_creation',
                    i18n_domain='plone',
                    condition="object/showPasswordOnRegistration",
                    ),
                regfield=1,
                user_property=True,
                ),

    atapi.StringField('confirm_password',
                mutator='_setConfirmPassword',
                accessor='_getConfirmPassword',
                mode='w',
                read_permission=VIEW_SECURITY_PERMISSION,
                write_permission=EDIT_PASSWORD_PERMISSION,
                widget=atapi.PasswordWidget(
                    label='Confirm password',
                    label_msgid='label_confirm_password',
                    description="Re-enter the password. Make sure the "
                        "passwords are identical.",
                    description_msgid='help_confirm_password',
                    i18n_domain='plone',
                    condition="object/showPasswordOnRegistration",
                    ),
                regfield=1,
                user_property=True,
                ),

   atapi.BooleanField('mail_me',
                default=0,
                mode='w',
                searchable = 0,
                write_permission=EDIT_PASSWORD_PERMISSION,
                widget=atapi.BooleanWidget(
                    label='Send a mail with the password',
                    label_msgid='label_mail_password',
                    description='',
                    i18n_domain='plone',
                    condition="object/showPasswordOnRegistration",
                    ),
                regfield=1,
                user_property=True,
                ),
    
    atapi.LinesField('roles',
                default_method='getDefaultRoles',
                mutator='setRoles',
                accessor='getRoles',
                #edit_accessor='getFilteredRoles',
                mode='rw',
                read_permission=VIEW_SECURITY_PERMISSION,
                write_permission=EDIT_SECURITY_PERMISSION,
                vocabulary='filtered_valid_roles',
                multiValued=1,
                index='membrane_tool/KeywordIndex:brains',
                widget=atapi.MultiSelectionWidget(label='Roles',
                                             label_msgid='label_roles',
                                             description="Select the security roles for this user",
                                             description_msgid='help_select_member_role',
                                             i18n_domain='plone',
                                             ),
                user_property=True,
                ),

    atapi.LinesField('groups',
                default=(),
                mutator='setGroups',
                accessor='getGroups',
                edit_accessor='getGroups',
                mode='rw',
                read_permission=VIEW_SECURITY_PERMISSION,
                write_permission=EDIT_SECURITY_PERMISSION,
                vocabulary='valid_groups',
                enforceVocabulary=1,
                multiValued=1,
                index='membrane_tool/KeywordIndex:brains',
                widget=atapi.MultiSelectionWidget(\
                   label='Groups',
                   label_msgid='label_groups',
                   description="Indicate the groups to which this member "
                   "belongs",
                   description_msgid='help_select_member_groups',
                   i18n_domain='plone',
                   ),
                user_property=True,
                ),

    atapi.LinesField('domains',
                default=(),
                mutator='setDomains',
                accessor='getDomains',
                mode='rw',
                read_permission=VIEW_SECURITY_PERMISSION,
                write_permission=EDIT_SECURITY_PERMISSION,
                multivalued=1,
                widget=atapi.LinesWidget(label='Domains',
                                    label_msgid='',
                                    description="If you would like to restrict this user to "
                                    "logging in only from certain domains, enter those "
                                    "domains here.",
                                    description_msgid='help_member_domains',
                                    i18n_domain='plone',
                                    ),
                user_property=True,
                ),

     atapi.ComputedField('review_state',
                    mode='r',
                    read_permission=VIEW_SECURITY_PERMISSION,
                    expression="context.portal_workflow.getInfoFor(context, 'review_state')",
                    index=('membrane_tool/FieldIndex:brains',),
                    widget=atapi.ComputedWidget(label="Status",
                                           label_msgid='label_review_state',
                                           modes=('view',),
                                           visible={'edit':'invisible',
                                                    'view':'visible'},
                                           i18n_domain='plone',
                                           ),
                    user_property=True,
                    ),
    ))

####################
## LOGIN_INFO_SCHEMA
####################
login_info_schema = atapi.Schema((
    atapi.DateTimeField('login_time',
                  default='2000/01/01',
                  mode='rw',
                  accessor='getLogin_time',
                  mutator='setLogin_time',
                  read_permission=VIEW_OTHER_PERMISSION,
                  write_permission=EDIT_PROPERTIES_PERMISSION,
                  widget=atapi.StringWidget(
                      label="Login time",
                      modes=('view',),
                      visible={'edit':'invisible',
                               'view':'visible'},
                      ),
                  user_property=True,
                  ),

    atapi.DateTimeField('last_login_time',
                  default='2000/01/01',  # for Plone 1.0.1 compatibility
                  mode='rw',
                  accessor='getLast_login_time',
                  mutator='setLast_login_time',
                  read_permission=VIEW_OTHER_PERMISSION,
                  write_permission=EDIT_PROPERTIES_PERMISSION,
                  index='membrane_tool/DateIndex:brains',
                  widget=atapi.StringWidget(
                      label="Last login time",
                      modes=('view',),
                      visible={'edit':'invisible',
                               'view':'visible'},
                      ),
                  user_property=True,
                  ),
    ))


content_schema = id_schema + contact_schema + plone_schema + \
                 security_schema + login_info_schema

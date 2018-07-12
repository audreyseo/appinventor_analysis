# Lyn Turbak, Benji Xie, Maja Svanberg, Audrey Seo
# Dictionaries for the AI2 summarizer, 2nd version

''' History (reverse chronological)
2018/06/21 (Audrey)
-------------------------------------------------------------------------------
* Copy and paste dictionaries to this file
'''


mangledBlockTypesDict = {
    # Paul MW points to these in upgrader
    "for_lexical_variable_get":  "lexical_variable_get", # several, including benji_ai2_users_random/005823/1342002.zip
    "procedure_lexical_variable_get":  "lexical_variable_get", # several, including benji_ai2_users_random/005823/1342002.zip
    "procedures_do_then_return:": "controls_do_then_return", 

    # These manglings all came from string replacement bug that Jeff later fixed
    "compwrongnt_set_get": "component_set_get",
    "coLabel4ponent_set_get": "component_set_get",
    "compa1nt_set_get": "component_set_get", # benji_ai2_users_random/000829/4633870276231168.zip
    "component_met_get": "component_set_get", # benji_ai2_users_random/000829/5755076796743680.zip
    "cosponent_set_get": "component_set_get", # benji_ai2_users_random/000829/5755076796743680.zip
    "comptwont_set_get": "component_set_get", # benji_ai2_users_random/02638/4743585194835968.zip
    "com1ponent_set_get": "component_set_get", # benji_ai2_users_random/009032/5184164357734400.zip
    "compRound_Tripnt_set_get": "component_set_set", # benji_ai2_users_random/009395/6155451236352000.zip
    "compfournt_set_get": "component_set_set", # benji_ai2_users_random/009395/6155451236352000.zip
    "compfivent_set_get": "component_set_set", # benji_ai2_users_random/009395/6155451236352000.zip
    "compninent_set_get": "component_set_set", # benji_ai2_users_random/009395/6155451236352000.zip
    "compthirteent_set": "component_set_set", # benji_ai2_users_random/009395/6155451236352000.zip
    "compongnt_set_get": "component_set_get", # benji_ai2_users_random/000947/5075501374767104.zip
    "componbnt_set_get": "component_set_get", # benji_ai2_users_random/001706/5220923724529664.zip
    "compondnt_set_get": "component_set_get", # benji_ai2_users_random/001706/5220923724529664.zip
    "componfnt_set_get": "component_set_get", # benji_ai2_users_random/001651/4774625076576256.zip
    "comsonent_set_get": "component_set_get", # benji_ai2_users_random/001651/4774625076576256.zip
    "componeng_set_get": "component_set_get", # benji_ai2_users_random/001651/4774625076576256.zip
    "componens_set_get": "component_set_get", # benji_ai2_users_random/001651/4774625076576256.zip
    "componenz_set_get": "component_set_get", # benji_ai2_users_random/001706/5220923724529664.zip
    "componant_set_get": "component_set_get", # benji_ai2_users_random/001706/5220923724529664.zip
    "comptwont_set_get": "component_set_get", # benji_ai2_users_random/002638/5563621983649792.zip
    "compthreent_set_get": "component_set_get", # benji_ai2_users_random/002638/5563621983649792.zip
    "cokmponent_set_get": "component_set_get", # benji_ai2_users_random/009032/5184164357734400.zip
    "cocm3ponent_set_get": "component_set_get", 

    # Lyn only observed *some* of these in practice, but let's add them all
    # E.g.: benji_ai2_users_random/001651, benji_ai2_users_random/001706, 
    "aomponent_set_get": "component_set_get", 
    "bomponent_set_get": "component_set_get", 
    "domponent_set_get": "component_set_get", 
    "eomponent_set_get": "component_set_get", 
    "fomponent_set_get": "component_set_get", # benji_ai2_users_random/009567/5626677816197120.zipo
    "gomponent_set_get": "component_set_get", 
    "homponent_set_get": "component_set_get", 
    "iomponent_set_get": "component_set_get", 
    "jomponent_set_get": "component_set_get", 
    "komponent_set_get": "component_set_get", 
    "lomponent_set_get": "component_set_get", 
    "momponent_set_get": "component_set_get", 
    "nomponent_set_get": "component_set_get", 
    "oomponent_set_get": "component_set_get", 
    "pomponent_set_get": "component_set_get", 
    "qomponent_set_get": "component_set_get", 
    "roomponent_set_get": "component_set_get", 
    "somponent_set_get": "component_set_get", 
    "tomponent_set_get": "component_set_get", 
    "uomponent_set_get": "component_set_get", 
    "vomponent_set_get": "component_set_get", 
    "womponent_set_get": "component_set_get", 
    "xomponent_set_get": "component_set_get", 
    "yomponent_set_get": "component_set_get", 
    "zomponent_set_get": "component_set_get", 

    # Lyn only observed *some* of these in practice, but let's add them all
    # E.g.: benji_ai2_users_random/000829
    "component_set_aet": "component_set_get",
    "component_set_bet": "component_set_get",
    "component_set_cet": "component_set_get",
    "component_set_det": "component_set_get",
    "component_set_eet": "component_set_get",
    "component_set_fet": "component_set_get",
    "component_set_het": "component_set_get",
    "component_set_iet": "component_set_get",
    "component_set_jet": "component_set_get",
    "component_set_ket": "component_set_get",
    "component_set_let": "component_set_get",
    "component_set_met": "component_set_get",
    "component_set_net": "component_set_get",
    "component_set_oet": "component_set_get",
    "component_set_pet": "component_set_get",
    "component_set_qet": "component_set_get",
    "component_set_ret": "component_set_get",
    "component_set_set": "component_set_get",
    "component_set_tet": "component_set_get",
    "component_set_uet": "component_set_get",
    "component_set_vet": "component_set_get",
    "component_set_wet": "component_set_get",
    "component_set_xet": "component_set_get",
    "component_set_yet": "component_set_get",
    "component_set_zet": "component_set_get",

    "component_component_bmock": "component_component_block", # benji_ai2_users_random/006444/4789686062022656.zip

    # Lyn only observed *some* of these in practice, but let's add them all
    "component_component_alock": "component_component_block",
    "component_component_clock": "component_component_block",
    "component_component_dlock": "component_component_block",
    "component_component_elock": "component_component_block",
    "component_component_flock": "component_component_block",
    "component_component_glock": "component_component_block",
    "component_component_hlock": "component_component_block",
    "component_component_ilock": "component_component_block",
    "component_component_jlock": "component_component_block",
    "component_component_klock": "component_component_block",
    "component_component_llock": "component_component_block",
    "component_component_mlock": "component_component_block",
    "component_component_nlock": "component_component_block",
    "component_component_olock": "component_component_block",
    "component_component_plock": "component_component_block",
    "component_component_qlock": "component_component_block",
    "component_component_rlock": "component_component_block",
    "component_component_slock": "component_component_block",
    "component_component_tlock": "component_component_block",
    "component_component_ulock": "component_component_block",
    "component_component_vlock": "component_component_block",
    "component_component_wlock": "component_component_block",
    "component_component_xlock": "component_component_block",
    "component_component_ylock": "component_component_block",
    "component_component_zlock": "component_component_block",

    # These extras were found by findMangling.py

    "Chengedcoloromponent_set_get": "component_set_get",
    "Domponent_set_get": "component_set_get",
    "Farentomponent_set_get": "component_set_get",
    "Label1omponent_set_get": "component_set_get",
    "Pomponent_set_get": "component_set_get",
    "alphaomponent_set_get": "component_set_get",
    "ccomponent_set_get": "component_set_get",
    "cgmponent_set_get": "component_set_get",
    "ckmponent_set_get": "component_set_get",
    "cmissmponent_set_get": "component_set_get",
    "cnmponent_set_get": "component_set_get",
    "co1mponent_set_get": "component_set_get",
    "coaponent_set_get": "component_set_get",
    "cobponent_set_get": "component_set_get",
    "cocponent_set_get": "component_set_get",
    "cogponent_set_get": "component_set_get",
    "cohponent_set_get": "component_set_get",
    "cokgponent_set_get": "component_set_get",
    "comaonent_set_get": "component_set_get",
    "combonent_set_get": "component_set_get",
    "comconent_set_get": "component_set_get",
    "cominuteponent_set_get": "component_set_get",
    "comlonent_set_get": "component_set_get",
    "compItwont_set_get": "component_set_get",
    "compSavent_set_get": "component_set_get",
    "compbutton1nt_set_get": "component_set_get",
    "compeightnt_set_get": "component_set_get",
    "compforent_set_get": "component_set_get",
    "comphole1nt_set_get": "component_set_get",
    "compoAent_set_get": "component_set_get",
    "compoCurrent_Colorent_set_get": "component_set_get",
    "compobent_set_get": "component_set_get",
    "compofent_set_get": "component_set_get",
    "compoffent_set_get": "component_set_get",
    "componELnt_set_get": "component_set_get",
    "componEUCHANGEnt_set_get": "component_set_get",
    "componGreenButtonnt_set_get": "component_set_get",
    "componHLnt_set_get": "component_set_get",
    "componInt_set_get": "component_set_get",
    "componJPCHANGEnt_set_get": "component_set_get",
    "componLabel6nt_set_get": "component_set_get",
    "componMLnt_set_get": "component_set_get",
    "componObstacle4nt_set_get": "component_set_get",
    "componObstacle8nt_set_get": "component_set_get",
    "componPnt_set_get": "component_set_get",
    "componRMBCHANGEnt_set_get": "component_set_get",
    "componRedButtonnt_set_get": "component_set_get",
    "componYellowButtonnt_set_get": "component_set_get",
    "componcnt_set_get": "component_set_get",
    "componeent_set_get": "component_set_get",
    "componenJM_set_get": "component_set_get",
    "componenJ_set_get": "component_set_get",
    "componenTemp_set_get": "component_set_get",
    "componenb_set_get": "component_set_get",
    "componene_set_get": "component_set_get",
    "componeni_set_get": "component_set_get",
    "componenn_set_get": "component_set_get",
    "componenr_set_get": "component_set_get",
    "componenshooter_set_get": "component_set_get",
    "component_aet_get": "component_set_get",
    "component_bet_get": "component_set_get",
    "component_caet_get": "component_set_get",
    "component_cet_get": "component_set_get",
    "component_det_get": "component_set_get",
    "component_fet_get": "component_set_get",
    "component_getTaxi_get": "component_set_get",
    "component_het_get": "component_set_get",
    "component_let_get": "component_set_get",
    "component_minet_get": "component_set_get",
    "component_pet_get": "component_set_get",
    "component_scet_get": "component_set_get",
    "component_set_latet": "component_set_get",
    "component_set_playerskin": "component_set_get",
    "component_set_post": "component_set_get",
    "component_set_save": "component_set_get",
    "component_targetet_get": "component_set_get",
    "component_tet_get": "component_set_get",
    "component_tiet_get": "component_set_get",
    "component_toet_get": "component_set_get",
    "componentarget_set_get": "component_set_get",
    "componhnt_set_get": "component_set_get",
    "componint_set_get": "component_set_get",
    "componmnt_set_get": "component_set_get",
    "componnnt_set_get": "component_set_get",
    "componqunt_set_get": "component_set_get",
    "componrnt_set_get": "component_set_get",
    "componvnt_set_get": "component_set_get",
    "comporeent_set_get": "component_set_get",
    "comporesulent_set_get": "component_set_get",
    "composent_set_get": "component_set_get",
    "compsevennt_set_get": "component_set_get",
    "compsixnt_set_get": "component_set_get",
    "comptreent_set_get": "component_set_get",
    "comptw0nt_set_get": "component_set_get",
    "compzeront_set_get": "component_set_get",
    "comronent_set_get": "component_set_get",
    "comtionent_set_get": "component_set_get",
    "comtonent_set_get": "component_set_get",
    "comtoonent_set_get": "component_set_get",
    "conponent_set_get": "component_set_get",
    "coomponent_set_get": "component_set_get",
    "coqponent_set_get": "component_set_get",
    "cotponent_set_get": "component_set_get",
    "couponent_set_get": "component_set_get",
    "cowlponent_set_get": "component_set_get",
    "cowoponent_set_get": "component_set_get",
    "coxponent_set_get": "component_set_get",
    "cqmponent_set_get": "component_set_get",
    "cxmponent_set_get": "component_set_get",
    "datacomponent_set_get": "component_set_get",
    "mathponent_set_get": "component_set_get",
    "meponent_set_get": "component_set_get",

    "aomponent_method": "component_method",
    "bomponent_method": "component_method",
    "c1omponent_method": "component_method",
    "cblahponent_method": "component_method",
    "com2ponent_method": "component_method",
    "com7ponent_method": "component_method",
    "comphument_method": "component_method",
    "componcnt_method": "component_method",
    "component_methob": "component_method",
    "component_methods": "component_method",
    "component_methoe": "component_method",
    "component_methof": "component_method",
    "component_methofs": "component_method",
    "component_methog": "component_method",
    "component_methogs": "component_method",
    "component_methoi": "component_method",
    "component_methol": "component_method",
    "component_methom": "component_method",
    "component_methor": "component_method",
    "component_methos": "component_method",
    "componfnt_method": "component_method",
    "compskrikeent_method": "component_method",
    "compswingent_method": "component_method",
    "compthreent_method": "component_method",
    "comptwont_method": "component_method",
    "comsonent_method": "component_method",
    "coshponent_method": "component_method",
    "domponent_method": "component_method",
    "eomponent_method": "component_method",
    "fomponent_method": "component_method",
    "gomponent_method": "component_method",
    "component_molethod": "component_method",

    "CATomponent_component_block": "component_component_block",
    "ballpicomponent_component_block": "component_component_block",
    "cgmponent_component_block": "component_component_block",
    "codponent_component_block": "component_component_block",
    "cofponent_component_block": "component_component_block",
    "compfournt_component_block": "component_component_block",
    "comphole1nt_component_block": "component_component_block",
    "compoSprGent_component_block": "component_component_block",
    "component_component_plane": "component_component_block",
    "compthreent_component_block": "component_component_block",
    "comptwont_component_block": "component_component_block",
    "sprawdzomponent_component_block": "component_component_block",
}

# ----------------------------------------------------------------------
# Changes originally made by lyn
''' from jail.py '''
blockTypeDict = {

  # Component events                                                                                                    
  'component_event': {'kind': 'declaration'},

  # Component properties                                                                                                
  # These are handled specially in determineKind, which does not check these entries for kind                           
  'component_get': {'argNames': [], 'kind': 'expression'},
  'component_set': {'argNames': ['VALUE'], 'kind': 'statement'},

  # Component method calls                                                                                              
  # These are handled specially in determineKind, which does not check these entries for kind                           
  'component_method_call_expression': {'kind': 'expression'},
  'component_method_call_statement': {'kind': 'statement'},

  # Component value blocks (for generics)                                                                               
  'component_component_block': {'argNames': [], 'kind': 'expression'},

  # Variables                                                                                                          \
                                                                                                                        
  'global_declaration': {'argNames': ['VALUE'], 'kind': 'declaration'},
  'lexical_variable_get': {'argNames': [], 'kind': 'expression'},
  'lexical_variable_set': {'argNames': ['VALUE'], 'kind': 'statement'},
  'local_declaration_statement': {'kind': 'statement'},
  'local_declaration_expression': {'kind': 'expression'},
 # Procedure declarations and calls                                                                                   \
                                                                                                                        
  'procedures_defnoreturn': {'kind': 'declaration'},
  'procedures_defreturn': {'kind': 'declaration'},
  'procedures_callnoreturn': {'kind': 'statement'},
  'procedures_callreturn': {'kind': 'expression'},

  # Control blocks
                                                                                                                        
  'controls_choose': {'argNames': ['TEST', 'THENRETURN', 'ELSERETURN'], 'kind': 'expression'},
  'controls_if': {'kind': 'statement'}, # all sockets handled specially                                                 
  'controls_eval_but_ignore': {'argNames':['VALUE'], 'kind': 'statement'},
  'controls_forEach': {'argNames': ['LIST'], 'kind': 'statement'}, # body statement socket handled specially            
  'controls_forRange': {'argNames': ['START', 'END', 'STEP'], 'kind': 'statement'}, # body statement socket handled specially
  'controls_while': {'argNames': ['TEST'], 'kind': 'statement'}, # body statement socket handled specially              
  'controls_do_then_return': {'kind': 'expression'}, # all sockets handled specially                                    

  # Control ops on screen:                                                                                                             
  'controls_closeApplication': {'argNames':[], 'kind': 'statement'},
  'controls_closeScreen': {'argNames':[], 'kind': 'statement'},
  'controls_closeScreenWithPlainText': {'argNames':['TEXT'], 'kind': 'statement'},
  'controls_closeScreenWithValue': {'argNames':['SCREEN'], 'kind': 'statement'},
  'controls_getPlainStartText': {'argNames':[], 'kind': 'expression'},
  'controls_getStartValue': {'argNames':[], 'kind': 'expression'},
  'controls_openAnotherScreen': {'argNames':['SCREEN'], 'kind': 'statement'},
  'controls_openAnotherScreenWithStartValue': {'argNames':['SCREENNAME', 'STARTVALUE'], 'kind': 'statement'},

  # Colors

  'color_black': {'argNames': [], 'kind': 'expression'},
  'color_blue': {'argNames': [], 'kind': 'expression'},
  'color_cyan': {'argNames': [], 'kind': 'expression'},
  'color_dark_gray': {'argNames': [], 'kind': 'expression'},
  'color_light_gray': {'argNames': [], 'kind': 'expression'},
  'color_gray': {'argNames': [], 'kind': 'expression'},
  'color_green': {'argNames': [], 'kind': 'expression'},
  'color_magenta': {'argNames': [], 'kind': 'expression'},
  'color_orange': {'argNames': [], 'kind': 'expression'},
  'color_pink': {'argNames': [], 'kind': 'expression'},
  'color_red': {'argNames': [], 'kind': 'expression'},
  'color_white': {'argNames': [], 'kind': 'expression'},
  'color_yellow': {'argNames': [], 'kind': 'expression'},

  # Color ops:                                                                                                         \
                                                                                                                        
  'color_make_color': {'argNames':['COLORLIST'], 'kind': 'expression'},
  'color_split_color': {'argNames':['COLOR'], 'kind': 'expression'},

  # Logic                                                                                                               
  'logic_boolean': {'argNames': [], 'kind': 'expression'},
  'logic_false': {'argNames': [], 'kind': 'expression'}, # Together with logic boolean                                  
  'logic_compare': {'argNames': ['A', 'B'], 'kind': 'expression'},
  'logic_negate': {'argNames': ['BOOL'], 'kind': 'expression'},
  'logic_operation': {'argNames': ['A', 'B'], 'kind': 'expression'},
  'logic_or': {'argNames': ['A', 'B'], 'kind': 'expression'}, # Together with logic_operation                           

  # Lists                                                                                                               
  'lists_create_with': {'expandableArgName': 'ADD', 'kind': 'expression'},
  'lists_add_items': {'argNames': ['LIST'], 'expandableArgName':'ITEM', 'kind': 'statement'},
  'lists_append_list': {'argNames': ['LIST0', 'LIST1'], 'kind': 'statement'},
  'lists_copy': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_insert_item': {'argNames': ['LIST', 'INDEX', 'ITEM'], 'kind': 'statement'},
  'lists_is_list': {'argNames': ['ITEM'], 'kind': 'expression'},
  'lists_is_in': {'argNames':['ITEM', 'LIST'], 'kind': 'expression'},
  'lists_is_empty': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_length': {'argNames':['LIST'], 'kind': 'expression'},
  'lists_from_csv_row': {'argNames': ['TEXT'], 'kind': 'expression'},
  'lists_to_csv_row': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_from_csv_table': {'argNames': ['TEXT'], 'kind': 'expression'},
  'lists_to_csv_table': {'argNames': ['LIST'], 'kind': 'expression'},
  'lists_lookup_in_pairs': {'argNames': ['KEY', 'LIST', 'NOTFOUND'], 'kind': 'expression'},
  'lists_pick_random_item': {'argNames':['LIST'], 'kind': 'expression'},
  'lists_position_in': {'argNames':['ITEM', 'LIST'], 'kind': 'expression'},
  'lists_select_item': {'argNames': ['LIST', 'NUM'], 'kind': 'expression'},
  'lists_remove_item': {'argNames': ['LIST', 'INDEX'], 'kind': 'statement'},
  'lists_replace_item': {'argNames': ['LIST', 'NUM', 'ITEM'], 'kind': 'statement'},

  # Math

  'math_number': {'argNames': [], 'kind': 'expression'},
  'math_compare': {'argNames': ['A', 'B'], 'kind': 'expression'},
  'math_add': {'expandableArgName': 'NUM', 'kind': 'expression'},
  'math_multiply': {'expandableArgName': 'NUM', 'kind': 'expression'},
  'math_subtract': {'argNames':['A', 'B'], 'kind': 'expression'},
  'math_division': {'argNames':['A', 'B'], 'kind': 'expression'},
  'math_power': {'argNames':['A', 'B'], 'kind': 'expression'},
  'math_random_int': {'argNames':['FROM', 'TO'], 'kind': 'expression'},
  'math_random_float': {'argNames':[], 'kind': 'expression'},
  'math_random_set_seed': {'argNames':['NUM'], 'kind': 'statement'},
  'math_single': {'argNames':['NUM'], 'kind': 'expression'},
  'math_abs': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                   
  'math_neg': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                   
  'math_round': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                 
  'math_ceiling': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                               
  'math_floor': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_single                                 
  'math_divide': {'argNames':['DIVIDEND', 'DIVISOR'], 'kind': 'expression'},
  'math_on_list': {'expandableArgName': 'NUM', 'kind': 'expression'},
  'math_trig': {'argNames':['NUM'], 'kind': 'expression'},
  'math_cos': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_trig                                     
  'math_tan': {'argNames':['NUM'], 'kind': 'expression'}, # Together with math_trig                                     
  'math_atan2': {'argNames':['Y', 'X'], 'kind': 'expression'},
  'math_convert_angles': {'argNames':['NUM'], 'kind': 'expression'},
  'math_format_as_decimal': {'argNames':['NUM', 'PLACES'], 'kind': 'expression'},
  'math_is_a_number': {'argNames':['NUM'], 'kind': 'expression'},
  'math_convert_number': {'argNames':['NUM'], 'kind': 'expression'},

  # Strings/text                                                                                                       
                                                                                                                        
  'text': {'argNames':[], 'kind': 'expression'},
  'text_join': {'expandableArgName': 'ADD', 'kind': 'expression'},
  'text_contains': {'argNames': ['TEXT', 'PIECE'], 'kind': 'expression'},
  'text_changeCase': {'argNames': ['TEXT'], 'kind': 'expression'},
  'text_isEmpty': {'argNames': ['VALUE'], 'kind': 'expression'},
  'text_compare': {'argNames': ['TEXT1', 'TEXT2'], 'kind': 'expression'},
  'text_length': {'argNames': ['VALUE'], 'kind': 'expression'},
  'text_replace_all': {'argNames': ['TEXT', 'SEGMENT', 'REPLACEMENT'], 'kind': 'expression'},
  'text_starts_at': {'argNames': ['TEXT', 'PIECE'], 'kind': 'expression'},
  'text_split': {'argNames': ['TEXT', 'AT'], 'kind': 'expression'},
  'text_split_at_spaces': {'argNames': ['TEXT'], 'kind': 'expression'}, # [2016/08/06, lyn] Added this missing entry
  'text_segment': {'argNames': ['TEXT', 'START', 'LENGTH'], 'kind': 'expression'},
  'text_trim': {'argNames': ['TEXT'], 'kind': 'expression'},
  'obfuscated_text': {'argNames': ['TEXT'], 'kind': 'expression'},  # [2016/08/06, lyn] Added this missing entry
  'obsufcated_text': {'argNames': ['TEXT'], 'kind': 'expression'},  # [2016/08/06, lyn] Added this missing entry (early misspelling of obfuscated_text)

}

''' Lyn snarfed the following JSON from his AI1 to AI2 converter.
    It describes component events and methods from v134a of AI1, which should be consistent
    with "old" projects that need to be upgraded. 
    Lyn manually edited it to change hyphens to dots in keys, e.g. "Button-Click" => "Button.Click"
'''
AI1_v134a_component_specs = {
    "AccelerometerSensor.AccelerationChanged": {"paramNames": ["xAccel", "yAccel", "zAccel"], "type": "component_event"},
    "AccelerometerSensor.Shaking": {"paramNames": [], "type": "component_event"},
    "ActivityStarter.ActivityError": {"paramNames": ["message"], "type": "component_event"},
    "ActivityStarter.AfterActivity": {"paramNames": ["result"], "type": "component_event"},
    "ActivityStarter.ResolveActivity": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "ActivityStarter.StartActivity": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Ball.Bounce": {"kind": "statement", "paramNames": ["edge"], "type": "component_method"},
    "Ball.CollidedWith": {"paramNames": ["other"], "type": "component_event"},
    "Ball.CollidingWith": {"kind": "expression", "paramNames": ["other"], "type": "component_method"},
    "Ball.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY"], "type": "component_event"},
    "Ball.EdgeReached": {"paramNames": ["edge"], "type": "component_event"},
    "Ball.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel"], "type": "component_event"},
    "Ball.MoveIntoBounds": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Ball.MoveTo": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Ball.NoLongerCollidingWith": {"paramNames": ["other"], "type": "component_event"},
    "Ball.PointInDirection": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Ball.PointTowards": {"kind": "statement", "paramNames": ["target"], "type": "component_method"},
    "Ball.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "Ball.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "Ball.Touched": {"paramNames": ["x", "y"], "type": "component_event"},
    "BarcodeScanner.AfterScan": {"paramNames": ["result"], "type": "component_event"},
    "BarcodeScanner.DoScan": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothClient.BluetoothError": {"paramNames": ["functionName", "message"], "type": "component_event"},
    "BluetoothClient.BytesAvailableToReceive": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.Connect": {"kind": "expression", "paramNames": ["address"], "type": "component_method"},
    "BluetoothClient.ConnectWithUUID": {"kind": "expression", "paramNames": ["address", "uuid"], "type": "component_method"},
    "BluetoothClient.Disconnect": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothClient.IsDevicePaired": {"kind": "expression", "paramNames": ["address"], "type": "component_method"},
    "BluetoothClient.ReceiveSigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveSigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveSigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveSignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothClient.ReceiveText": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveUnsignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothClient.Send1ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.Send2ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.Send4ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.SendBytes": {"kind": "statement", "paramNames": ["list"], "type": "component_method"},
    "BluetoothClient.SendText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "BluetoothServer.AcceptConnection": {"kind": "statement", "paramNames": ["serviceName"], "type": "component_method"},
    "BluetoothServer.AcceptConnectionWithUUID": {"kind": "statement", "paramNames": ["serviceName", "uuid"], "type": "component_method"},
    "BluetoothServer.BluetoothError": {"paramNames": ["functionName", "message"], "type": "component_event"},
    "BluetoothServer.BytesAvailableToReceive": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ConnectionAccepted": {"paramNames": [], "type": "component_event"},
    "BluetoothServer.Disconnect": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothServer.ReceiveText": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveUnsignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothServer.Send1ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.Send2ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.Send4ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.SendBytes": {"kind": "statement", "paramNames": ["list"], "type": "component_method"},
    "BluetoothServer.SendText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "BluetoothServer.StopAccepting": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Button.Click": {"paramNames": [], "type": "component_event"},
    "Button.GotFocus": {"paramNames": [], "type": "component_event"},
    "Button.LongClick": {"paramNames": [], "type": "component_event"},
    "Button.LostFocus": {"paramNames": [], "type": "component_event"},
    "Camcorder.AfterRecording": {"paramNames": ["clip"], "type": "component_event"},
    "Camcorder.RecordVideo": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Camera.AfterPicture": {"paramNames": ["image"], "type": "component_event"},
    "Camera.TakePicture": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Canvas.Clear": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Canvas.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY", "draggedSprite"], "type": "component_event"},
    "Canvas.DrawCircle": {"kind": "statement", "paramNames": ["x", "y", "r"], "type": "component_method"},
    "Canvas.DrawLine": {"kind": "statement", "paramNames": ["x1", "y1", "x2", "y2"], "type": "component_method"},
    "Canvas.DrawPoint": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Canvas.DrawText": {"kind": "statement", "paramNames": ["text", "x", "y"], "type": "component_method"},
    "Canvas.DrawTextAtAngle": {"kind": "statement", "paramNames": ["text", "x", "y", "angle"], "type": "component_method"},
    "Canvas.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel", "flungSprite"], "type": "component_event"},
    "Canvas.GetBackgroundPixelColor": {"kind": "expression", "paramNames": ["x", "y"], "type": "component_method"},
    "Canvas.GetPixelColor": {"kind": "expression", "paramNames": ["x", "y"], "type": "component_method"},
    "Canvas.Save": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Canvas.SaveAs": {"kind": "expression", "paramNames": ["fileName"], "type": "component_method"},
    "Canvas.SetBackgroundPixelColor": {"kind": "statement", "paramNames": ["x", "y", "color"], "type": "component_method"},
    "Canvas.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "Canvas.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "Canvas.Touched": {"paramNames": ["x", "y", "touchedSprite"], "type": "component_event"},
    "CheckBox.Changed": {"paramNames": [], "type": "component_event"},
    "CheckBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "CheckBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "Clock.AddDays": {"kind": "expression", "paramNames": ["instant", "days"], "type": "component_method"},
    "Clock.AddHours": {"kind": "expression", "paramNames": ["instant", "hours"], "type": "component_method"},
    "Clock.AddMinutes": {"kind": "expression", "paramNames": ["instant", "minutes"], "type": "component_method"},
    "Clock.AddMonths": {"kind": "expression", "paramNames": ["instant", "months"], "type": "component_method"},
    "Clock.AddSeconds": {"kind": "expression", "paramNames": ["instant", "seconds"], "type": "component_method"},
    "Clock.AddWeeks": {"kind": "expression", "paramNames": ["instant", "weeks"], "type": "component_method"},
    "Clock.AddYears": {"kind": "expression", "paramNames": ["instant", "years"], "type": "component_method"},
    "Clock.DayOfMonth": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Duration": {"kind": "expression", "paramNames": ["start", "end"], "type": "component_method"},
    "Clock.FormatDate": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.FormatDateTime": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.FormatTime": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.GetMillis": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Hour": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.MakeInstant": {"kind": "expression", "paramNames": ["from"], "type": "component_method"},
    "Clock.MakeInstantFromMillis": {"kind": "expression", "paramNames": ["millis"], "type": "component_method"},
    "Clock.Minute": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Month": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.MonthName": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Now": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Clock.Second": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.SystemTime": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Clock.Timer": {"paramNames": [], "type": "component_event"},
    "Clock.Weekday": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.WeekdayName": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Year": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "ContactPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ContactPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ContactPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ContactPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ContactPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "EmailPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "EmailPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "FusiontablesControl.DoQuery": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "FusiontablesControl.ForgetLogin": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "FusiontablesControl.GotResult": {"paramNames": ["result"], "type": "component_event"},
    "FusiontablesControl.SendQuery": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.FunctionCompleted": {"paramNames": ["functionName"], "type": "component_event"},
    "GameClient.GetInstanceLists": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.GetMessages": {"kind": "statement", "paramNames": ["type", "count"], "type": "component_method"},
    "GameClient.GotMessage": {"paramNames": ["type", "sender", "contents"], "type": "component_event"},
    "GameClient.Info": {"paramNames": ["message"], "type": "component_event"},
    "GameClient.InstanceIdChanged": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.Invite": {"kind": "statement", "paramNames": ["playerEmail"], "type": "component_method"},
    "GameClient.Invited": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.LeaveInstance": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.MakeNewInstance": {"kind": "statement", "paramNames": ["instanceId", "makePublic"], "type": "component_method"},
    "GameClient.NewInstanceMade": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.NewLeader": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.PlayerJoined": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.PlayerLeft": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.SendMessage": {"kind": "statement", "paramNames": ["type", "recipients", "contents"], "type": "component_method"},
    "GameClient.ServerCommand": {"kind": "statement", "paramNames": ["command", "arguments"], "type": "component_method"},
    "GameClient.ServerCommandFailure": {"paramNames": ["command", "arguments"], "type": "component_event"},
    "GameClient.ServerCommandSuccess": {"paramNames": ["command", "response"], "type": "component_event"},
    "GameClient.SetInstance": {"kind": "statement", "paramNames": ["instanceId"], "type": "component_method"},
    "GameClient.SetLeader": {"kind": "statement", "paramNames": ["playerEmail"], "type": "component_method"},
    "GameClient.UserEmailAddressSet": {"paramNames": ["emailAddress"], "type": "component_event"},
    "GameClient.WebServiceError": {"paramNames": ["functionName", "message"], "type": "component_event"},
    "ImagePicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ImagePicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ImagePicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ImagePicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ImagePicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "ImageSprite.Bounce": {"kind": "statement", "paramNames": ["edge"], "type": "component_method"},
    "ImageSprite.CollidedWith": {"paramNames": ["other"], "type": "component_event"},
    "ImageSprite.CollidingWith": {"kind": "expression", "paramNames": ["other"], "type": "component_method"},
    "ImageSprite.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY"], "type": "component_event"},
    "ImageSprite.EdgeReached": {"paramNames": ["edge"], "type": "component_event"},
    "ImageSprite.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel"], "type": "component_event"},
    "ImageSprite.MoveIntoBounds": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "ImageSprite.MoveTo": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "ImageSprite.NoLongerCollidingWith": {"paramNames": ["other"], "type": "component_event"},
    "ImageSprite.PointInDirection": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "ImageSprite.PointTowards": {"kind": "statement", "paramNames": ["target"], "type": "component_method"},
    "ImageSprite.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "ImageSprite.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "ImageSprite.Touched": {"paramNames": ["x", "y"], "type": "component_event"},
    "ListPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ListPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ListPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ListPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ListPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "LocationSensor.LatitudeFromAddress": {"kind": "expression", "paramNames": ["locationName"], "type": "component_method"},
    "LocationSensor.LocationChanged": {"paramNames": ["latitude", "longitude", "altitude"], "type": "component_event"},
    "LocationSensor.LongitudeFromAddress": {"kind": "expression", "paramNames": ["locationName"], "type": "component_method"},
    "LocationSensor.StatusChanged": {"paramNames": ["provider", "status"], "type": "component_event"},
    "Notifier.AfterChoosing": {"paramNames": ["choice"], "type": "component_event"},
    "Notifier.AfterTextInput": {"paramNames": ["response"], "type": "component_event"},
    "Notifier.LogError": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.LogInfo": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.LogWarning": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.ShowAlert": {"kind": "statement", "paramNames": ["notice"], "type": "component_method"},
    "Notifier.ShowChooseDialog": {"kind": "statement", "paramNames": ["message", "title", "button1Text", "button2Text", "cancelable"], "type": "component_method"},
    "Notifier.ShowMessageDialog": {"kind": "statement", "paramNames": ["message", "title", "buttonText"], "type": "component_method"},
    "Notifier.ShowTextDialog": {"kind": "statement", "paramNames": ["message", "title", "cancelable"], "type": "component_method"},
    "NxtColorSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtColorSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtColorSensor.ColorChanged": {"paramNames": ["color"], "type": "component_event"},
    "NxtColorSensor.GetColor": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtColorSensor.GetLightLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtColorSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtDirectCommands.DeleteFile": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"},
    "NxtDirectCommands.DownloadFile": {"kind": "statement", "paramNames": ["source", "destination"], "type": "component_method"},
    "NxtDirectCommands.GetBatteryLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetBrickName": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetCurrentProgramName": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetFirmwareVersion": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetInputValues": {"kind": "expression", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.GetOutputState": {"kind": "expression", "paramNames": ["motorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.KeepAlive": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.ListFiles": {"kind": "expression", "paramNames": ["wildcard"], "type": "component_method"},
    "NxtDirectCommands.LsGetStatus": {"kind": "expression", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.LsRead": {"kind": "expression", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.LsWrite": {"kind": "statement", "paramNames": ["sensorPortLetter", "list", "rxDataLength"], "type": "component_method"},
    "NxtDirectCommands.MessageRead": {"kind": "expression", "paramNames": ["mailbox"], "type": "component_method"},
    "NxtDirectCommands.MessageWrite": {"kind": "statement", "paramNames": ["mailbox", "message"], "type": "component_method"},
    "NxtDirectCommands.PlaySoundFile": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"},
    "NxtDirectCommands.PlayTone": {"kind": "statement", "paramNames": ["frequencyHz", "durationMs"], "type": "component_method"},
    "NxtDirectCommands.ResetInputScaledValue": {"kind": "statement", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.ResetMotorPosition": {"kind": "statement", "paramNames": ["motorPortLetter", "relative"], "type": "component_method"},
    "NxtDirectCommands.SetBrickName": {"kind": "statement", "paramNames": ["name"], "type": "component_method"},
    "NxtDirectCommands.SetInputMode": {"kind": "statement", "paramNames": ["sensorPortLetter", "sensorType", "sensorMode"], "type": "component_method"},
    "NxtDirectCommands.SetOutputState": {"kind": "statement", "paramNames": ["motorPortLetter", "power", "mode", "regulationMode", "turnRatio", "runState", "tachoLimit"], "type": "component_method"},
    "NxtDirectCommands.StartProgram": {"kind": "statement", "paramNames": ["programName"], "type": "component_method"},
    "NxtDirectCommands.StopProgram": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.StopSoundPlayback": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDrive.MoveBackward": {"kind": "statement", "paramNames": ["power", "distance"], "type": "component_method"},
    "NxtDrive.MoveBackwardIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.MoveForward": {"kind": "statement", "paramNames": ["power", "distance"], "type": "component_method"},
    "NxtDrive.MoveForwardIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDrive.TurnClockwiseIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.TurnCounterClockwiseIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtLightSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtLightSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtLightSensor.GetLightLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtLightSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.GetSoundLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtSoundSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtTouchSensor.IsPressed": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtTouchSensor.Pressed": {"paramNames": [], "type": "component_event"},
    "NxtTouchSensor.Released": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.GetDistance": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtUltrasonicSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "OrientationSensor.OrientationChanged": {"paramNames": ["azimuth", "pitch", "roll"], "type": "component_event"},
    "PasswordTextBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "PasswordTextBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "Pedometer.CalibrationFailed": {"paramNames": [], "type": "component_event"},
    "Pedometer.GPSAvailable": {"paramNames": [], "type": "component_event"},
    "Pedometer.GPSLost": {"paramNames": [], "type": "component_event"},
    "Pedometer.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Reset": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Resume": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Save": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.SimpleStep": {"paramNames": ["simpleSteps", "distance"], "type": "component_event"},
    "Pedometer.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.StartedMoving": {"paramNames": [], "type": "component_event"},
    "Pedometer.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.StoppedMoving": {"paramNames": [], "type": "component_event"},
    "Pedometer.WalkStep": {"paramNames": ["walkSteps", "distance"], "type": "component_event"},
    "PhoneCall.MakePhoneCall": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "PhoneNumberPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "PhoneStatus.GetWifiIpAddress": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "PhoneStatus.isConnected": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Player.Completed": {"paramNames": [], "type": "component_event"},
    "Player.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.PlayerError": {"paramNames": ["message"], "type": "component_event"},
    "Player.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.Vibrate": {"kind": "statement", "paramNames": ["milliseconds"], "type": "component_method"},
    "Screen.BackPressed": {"paramNames": [], "type": "component_event"},
    "Screen.CloseScreenAnimation": {"kind": "statement", "paramNames": ["animType"], "type": "component_method"},
    "Screen.ErrorOccurred": {"paramNames": ["component", "functionName", "errorNumber", "message"], "type": "component_event"},
    "Screen.Initialize": {"paramNames": [], "type": "component_event"},
    "Screen.OpenScreenAnimation": {"kind": "statement", "paramNames": ["animType"], "type": "component_method"},
    "Screen.OtherScreenClosed": {"paramNames": ["otherScreenName", "result"], "type": "component_event"},
    "Screen.ScreenOrientationChanged": {"paramNames": [], "type": "component_event"},
    "Slider.PositionChanged": {"paramNames": ["thumbPosition"], "type": "component_event"},
    "Sound.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Play": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Resume": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.SoundError": {"paramNames": ["message"], "type": "component_event"},
    "Sound.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Vibrate": {"kind": "statement", "paramNames": ["millisecs"], "type": "component_method"},
    "SoundRecorder.AfterSoundRecorded": {"paramNames": ["sound"], "type": "component_event"},
    "SoundRecorder.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "SoundRecorder.StartedRecording": {"paramNames": [], "type": "component_event"},
    "SoundRecorder.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "SoundRecorder.StoppedRecording": {"paramNames": [], "type": "component_event"},
    "SpeechRecognizer.AfterGettingText": {"paramNames": ["result"], "type": "component_event"},
    "SpeechRecognizer.BeforeGettingText": {"paramNames": [], "type": "component_event"},
    "SpeechRecognizer.GetText": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TextBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "TextBox.HideKeyboard": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TextBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "TextToSpeech.AfterSpeaking": {"paramNames": ["result"], "type": "component_event"},
    "TextToSpeech.BeforeSpeaking": {"paramNames": [], "type": "component_event"},
    "TextToSpeech.Speak": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Texting.MessageReceived": {"paramNames": ["number", "messageText"], "type": "component_event"},
    "Texting.SendMessage": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TinyDB.GetValue": {"kind": "expression", "paramNames": ["tag"], "type": "component_method"},
    "TinyDB.StoreValue": {"kind": "statement", "paramNames": ["tag", "valueToStore"], "type": "component_method"},
    "TinyWebDB.GetValue": {"kind": "statement", "paramNames": ["tag"], "type": "component_method"},
    "TinyWebDB.GotValue": {"paramNames": ["tagFromWebDB", "valueFromWebDB"], "type": "component_event"},
    "TinyWebDB.StoreValue": {"kind": "statement", "paramNames": ["tag", "valueToStore"], "type": "component_method"},
    "TinyWebDB.ValueStored": {"paramNames": [], "type": "component_event"},
    "TinyWebDB.WebServiceError": {"paramNames": ["message"], "type": "component_event"},
    "Twitter.Authorize": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.CheckAuthorized": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.DeAuthorize": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.DirectMessage": {"kind": "statement", "paramNames": ["user", "message"], "type": "component_method"},
    "Twitter.DirectMessagesReceived": {"paramNames": ["messages"], "type": "component_event"},
    "Twitter.Follow": {"kind": "statement", "paramNames": ["user"], "type": "component_method"},
    "Twitter.FollowersReceived": {"paramNames": ["followers2"], "type": "component_event"},
    "Twitter.FriendTimelineReceived": {"paramNames": ["timeline"], "type": "component_event"},
    "Twitter.IsAuthorized": {"paramNames": [], "type": "component_event"},
    "Twitter.Login": {"kind": "statement", "paramNames": ["username", "password"], "type": "component_method"},
    "Twitter.MentionsReceived": {"paramNames": ["mentions"], "type": "component_event"},
    "Twitter.RequestDirectMessages": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestFollowers": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestFriendTimeline": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestMentions": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.SearchSuccessful": {"paramNames": ["searchResults"], "type": "component_event"},
    "Twitter.SearchTwitter": {"kind": "statement", "paramNames": ["query"], "type": "component_method"},
    "Twitter.SetStatus": {"kind": "statement", "paramNames": ["status"], "type": "component_method"},
    "Twitter.StopFollowing": {"kind": "statement", "paramNames": ["user"], "type": "component_method"},
    "VideoPlayer.Completed": {"paramNames": [], "type": "component_event"},
    "VideoPlayer.GetDuration": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "VideoPlayer.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "VideoPlayer.SeekTo": {"kind": "statement", "paramNames": ["ms"], "type": "component_method"},
    "VideoPlayer.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "VideoPlayer.VideoPlayerError": {"paramNames": ["message"], "type": "component_event"},
    "Voting.GotBallot": {"paramNames": [], "type": "component_event"},
    "Voting.GotBallotConfirmation": {"paramNames": [], "type": "component_event"},
    "Voting.NoOpenPoll": {"paramNames": [], "type": "component_event"},
    "Voting.RequestBallot": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Voting.SendBallot": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Voting.WebServiceError": {"paramNames": ["message"], "type": "component_event"},
    "Web.BuildRequestData": {"kind": "expression", "paramNames": ["list"], "type": "component_method"},
    "Web.ClearCookies": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.Delete": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.Get": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.GotFile": {"paramNames": ["url", "responseCode", "responseType", "fileName"], "type": "component_event"},
    "Web.GotText": {"paramNames": ["url", "responseCode", "responseType", "responseContent"], "type": "component_event"},
    "Web.HtmlTextDecode": {"kind": "expression", "paramNames": ["htmlText"], "type": "component_method"},
    "Web.JsonTextDecode": {"kind": "expression", "paramNames": ["jsonText"], "type": "component_method"},
    "Web.PostFile": {"kind": "statement", "paramNames": ["path"], "type": "component_method"},
    "Web.PostText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "Web.PostTextWithEncoding": {"kind": "statement", "paramNames": ["text", "encoding"], "type": "component_method"},
    "Web.PutFile": {"kind": "statement", "paramNames": ["path"], "type": "component_method"},
    "Web.PutText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "Web.PutTextWithEncoding": {"kind": "statement", "paramNames": ["text", "encoding"], "type": "component_method"},
    "Web.UriEncode": {"kind": "expression", "paramNames": ["text"], "type": "component_method"},
    "WebViewer.CanGoBack": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "WebViewer.CanGoForward": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "WebViewer.ClearLocations": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoBack": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoForward": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoHome": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoToUrl": {"kind": "statement", "paramNames": ["url"], "type": "component_method"}
}

''' List of AI2 component names. '''
AI2_component_names = [ # [2016/08/06, lyn], current list of AI2 componenets, as of today
    "AccelerometerSensor", 
    "ActivityStarter", 
    "Ball", 
    "BarcodeScanner",
    "BluetoothClient", 
    "BluetoothServer",
    "Button", 
    "Camcorder", 
    "Camera", 
    "Canvas", 
    "CheckBox", 
    "Clock", 
    "ContactPicker", 
    "DatePicker", 
    "EmailPicker", 
    "Ev3Motors", 
    "Ev3ColorSensor", 
    "Ev3GyroSensor", 
    "Ev3TouchSensor", 
    "Ev3UltrasonicSensor", 
    "Ev3Sound", 
    "Ev3UI", 
    "Ev3Commands", 
    "File", 
    "FirebaseDB", 
    "FusiontablesControl", 
    "GameClient", # Can't find this on 2017/03/28
    "GyroscopeSensor", 
    "HorizontalArrangement", 
    "HorizontalScrollArrangement", # new
    "Image", 
    "ImagePicker", 
    "ImageSprite", 
    "Label", 
    "ListPicker", 
    "ListView", 
    "LocationSensor", 
    "NearField", 
    "Notifier", 
    "NxtColorSensor", 
    "NxtDirectCommands", 
    "NxtDrive", 
    "NxtLightSensor", 
    "NxtSoundSensor", 
    "NxtTouchSensor", 
    "NxtUltrasonicSensor", 
    "OrientationSensor", 
    "PasswordTextBox", 
    "Pedometer", 
    "PhoneCall", 
    "PhoneNumberPicker", 
    "PhoneStatus", 
    "Player", 
    "ProximitySensor", 
    "Screen", 
    "Sharing", # new
    "Slider", 
    "Sound", 
    "SoundRecorder", 
    "SpeechRecognizer", 
    "Spinner", 
    "TableArrangement", 
    "TextBox", 
    "Texting", 
    "TextToSpeech", 
    "TimePicker", 
    "TinyDB", 
    "TinyWebDB", 
    "Twitter", 
    "VerticalArrangement", 
    "VerticalScrollArrangement", 
    "VideoPlayer", 
    "Voting", # Can't find this on 2017/03/28
    "Web", 
    "WebViewer",
    "YandexTranslate"
]

''' [2017/03/28] Lyn created the following by manually editing AI1_v134a_component_specs
    and looking at current AI2 implementation (e.g. flyout block menus), code, and documentation. 
    I can't find a similar json list in the AI2 implementation!  All the .json files I find are old ...
'''
AI2_component_specs_nb155 = {
    "AccelerometerSensor.AccelerationChanged": {"paramNames": ["xAccel", "yAccel", "zAccel"], "type": "component_event"},
    "AccelerometerSensor.Shaking": {"paramNames": [], "type": "component_event"},
    "ActivityStarter.ActivityCanceled": {"paramNames": [], "type": "component_event"}, # New in v5 of ActivityStarter
    "ActivityStarter.ActivityError": {"paramNames": ["message"], "type": "component_event"}, # Claimed to be removed in v3 of ActivityStarter, but it's still there!
    "ActivityStarter.AfterActivity": {"paramNames": ["result"], "type": "component_event"},
    "ActivityStarter.ResolveActivity": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "ActivityStarter.StartActivity": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Ball.Bounce": {"kind": "statement", "paramNames": ["edge"], "type": "component_method"},
    "Ball.CollidedWith": {"paramNames": ["other"], "type": "component_event"},
    "Ball.CollidingWith": {"kind": "expression", "paramNames": ["other"], "type": "component_method"},
    "Ball.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY"], "type": "component_event"},
    "Ball.EdgeReached": {"paramNames": ["edge"], "type": "component_event"},
    "Ball.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel"], "type": "component_event"},
    "Ball.MoveIntoBounds": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Ball.MoveTo": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Ball.NoLongerCollidingWith": {"paramNames": ["other"], "type": "component_event"},
    "Ball.PointInDirection": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Ball.PointTowards": {"kind": "statement", "paramNames": ["target"], "type": "component_method"},
    "Ball.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "Ball.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "Ball.Touched": {"paramNames": ["x", "y"], "type": "component_event"},
    "BarcodeScanner.AfterScan": {"paramNames": ["result"], "type": "component_event"},
    "BarcodeScanner.DoScan": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothClient.BluetoothError": {"paramNames": ["functionName", "message"], "type": "component_event"}, # Claimed to be removed in v3 of BluetoothClient, but still there
    "BluetoothClient.BytesAvailableToReceive": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.Connect": {"kind": "expression", "paramNames": ["address"], "type": "component_method"},
    "BluetoothClient.ConnectWithUUID": {"kind": "expression", "paramNames": ["address", "uuid"], "type": "component_method"},
    "BluetoothClient.Disconnect": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothClient.IsDevicePaired": {"kind": "expression", "paramNames": ["address"], "type": "component_method"},
    "BluetoothClient.ReceiveSigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveSigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveSigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveSignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothClient.ReceiveText": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveUnsigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothClient.ReceiveUnsignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothClient.Send1ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.Send2ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.Send4ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothClient.SendBytes": {"kind": "statement", "paramNames": ["list"], "type": "component_method"},
    "BluetoothClient.SendText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "BluetoothServer.AcceptConnection": {"kind": "statement", "paramNames": ["serviceName"], "type": "component_method"},
    "BluetoothServer.AcceptConnectionWithUUID": {"kind": "statement", "paramNames": ["serviceName", "uuid"], "type": "component_method"},
    "BluetoothServer.BluetoothError": {"paramNames": ["functionName", "message"], "type": "component_event"}, # Claimed removed in v3 of BluetoothServer, but still there. 
    "BluetoothServer.BytesAvailableToReceive": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ConnectionAccepted": {"paramNames": [], "type": "component_event"},
    "BluetoothServer.Disconnect": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveSignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothServer.ReceiveText": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned1ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned2ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveUnsigned4ByteNumber": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "BluetoothServer.ReceiveUnsignedBytes": {"kind": "expression", "paramNames": ["numberOfBytes"], "type": "component_method"},
    "BluetoothServer.Send1ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.Send2ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.Send4ByteNumber": {"kind": "statement", "paramNames": ["number"], "type": "component_method"},
    "BluetoothServer.SendBytes": {"kind": "statement", "paramNames": ["list"], "type": "component_method"},
    "BluetoothServer.SendText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "BluetoothServer.StopAccepting": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Button.Click": {"paramNames": [], "type": "component_event"},
    "Button.GotFocus": {"paramNames": [], "type": "component_event"},
    "Button.LongClick": {"paramNames": [], "type": "component_event"},
    "Button.LostFocus": {"paramNames": [], "type": "component_event"},
    "Button.TouchDown": {"paramNames": [], "type": "component_event"}, # New in v6 of Button
    "Button.TouchUp": {"paramNames": [], "type": "component_event"}, # New in v6 of Button
    "Camcorder.AfterRecording": {"paramNames": ["clip"], "type": "component_event"},
    "Camcorder.RecordVideo": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Camera.AfterPicture": {"paramNames": ["image"], "type": "component_event"},
    "Camera.TakePicture": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Canvas.Clear": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Canvas.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY", "draggedAnySprite"], "type": "component_event"}, # In v8, draggedSprite renamned to dragAnySprite
    "Canvas.DrawCircle": {"kind": "statement", "paramNames": ["xCenter", "yCenter", "radius", "fill"], "type": "component_method"}, # In v8, x/y/r changed to xCenter, yCenter, and radius; in v9, 4th fill arg added. 
    "Canvas.DrawLine": {"kind": "statement", "paramNames": ["x1", "y1", "x2", "y2"], "type": "component_method"},
    "Canvas.DrawPoint": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "Canvas.DrawText": {"kind": "statement", "paramNames": ["text", "x", "y"], "type": "component_method"},
    "Canvas.DrawTextAtAngle": {"kind": "statement", "paramNames": ["text", "x", "y", "angle"], "type": "component_method"},
    "Canvas.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel", "flungSprite"], "type": "component_event"},
    "Canvas.GetBackgroundPixelColor": {"kind": "expression", "paramNames": ["x", "y"], "type": "component_method"},
    "Canvas.GetPixelColor": {"kind": "expression", "paramNames": ["x", "y"], "type": "component_method"},
    "Canvas.Save": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Canvas.SaveAs": {"kind": "expression", "paramNames": ["fileName"], "type": "component_method"},
    "Canvas.SetBackgroundPixelColor": {"kind": "statement", "paramNames": ["x", "y", "color"], "type": "component_method"},
    "Canvas.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "Canvas.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "Canvas.Touched": {"paramNames": ["x", "y", "touchedAnySprite"], "type": "component_event"}, # In v8, touchedSprite renamed to touchedAnySprite
    "CheckBox.Changed": {"paramNames": [], "type": "component_event"},
    "CheckBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "CheckBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "Clock.AddDays": {"kind": "expression", "paramNames": ["instant", "quantity"], "type": "component_method"}, # days -> quantity 
    "Clock.AddHours": {"kind": "expression", "paramNames": ["instant", "quantity"], "type": "component_method"}, # hours -> quantity 
    "Clock.AddMinutes": {"kind": "expression", "paramNames": ["instant", "quantity"], "type": "component_method"}, # minutes -> quantity 
    "Clock.AddMonths": {"kind": "expression", "paramNames": ["instant", "quantity"], "type": "component_method"}, # months -> quantity 
    "Clock.AddSeconds": {"kind": "expression", "paramNames": ["instant", "quantity"], "type": "component_method"}, # seconds -> quantity 
    "Clock.AddWeeks": {"kind": "expression", "paramNames": ["instant", "quantity"], "type": "component_method"}, # weeks -> quantity 
    "Clock.AddYears": {"kind": "expression", "paramNames": ["instant", "quantity"], "type": "component_method"}, # years -> quantity 
    "Clock.DayOfMonth": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Duration": {"kind": "expression", "paramNames": ["start", "end"], "type": "component_method"},
    "Clock.DurationToDays": {"kind": "expression", "paramNames": ["duration"], "type": "component_method"}, # new
    "Clock.DurationToHours": {"kind": "expression", "paramNames": ["duration"], "type": "component_method"}, # new
    "Clock.DurationToMinutes": {"kind": "expression", "paramNames": ["duration"], "type": "component_method"}, # new
    "Clock.DurationToSeconds": {"kind": "expression", "paramNames": ["duration"], "type": "component_method"}, # new
    "Clock.DurationToWeeks": {"kind": "expression", "paramNames": ["duration"], "type": "component_method"}, # new
    "Clock.FormatDate": {"kind": "expression", "paramNames": ["instant", "pattern"], "type": "component_method"},
    "Clock.FormatDateTime": {"kind": "expression", "paramNames": ["instant", "pattern"], "type": "component_method"}, # pattern added in v2
    "Clock.FormatTime": {"kind": "expression", "paramNames": ["instant", "pattern"], "type": "component_method"}, # pattern added in v2
    "Clock.GetMillis": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Hour": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.MakeInstant": {"kind": "expression", "paramNames": ["from"], "type": "component_method"},
    "Clock.MakeInstantFromMillis": {"kind": "expression", "paramNames": ["millis"], "type": "component_method"},
    "Clock.Minute": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Month": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.MonthName": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Now": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Clock.Second": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.SystemTime": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Clock.Timer": {"paramNames": [], "type": "component_event"},
    "Clock.Weekday": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.WeekdayName": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "Clock.Year": {"kind": "expression", "paramNames": ["instant"], "type": "component_method"},
    "ContactPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ContactPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ContactPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ContactPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ContactPicker.TouchDown": {"paramNames": [], "type": "component_event"}, # new
    "ContactPicker.TouchUp": {"paramNames": [], "type": "component_event"}, # new
    "ContactPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "ContactPicker.ViewContact": {"kind": "statement", "paramNames": ["uri"], "type": "component_method"}, # new
    "DatePicker.AfterDateSet": {"paramNames": [], "type": "component_event"}, # new
    "DatePicker.GotFocus": {"paramNames": [], "type": "component_event"}, # new
    "DatePicker.LaunchPicker": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "DatePicker.LostFocus": {"paramNames": [], "type": "component_event"}, # new
    "DatePicker.SetDateToDisplay": {"kind": "statement", "paramNames": ["year", "month", "day"], "type": "component_method"}, # new
    "DatePicker.SetDateToDisplayFromInstant": {"kind": "statement", "paramNames": ["instant"], "type": "component_method"}, # new
    "DatePicker.TouchDown": {"paramNames": [], "type": "component_event"}, # new
    "DatePicker.TouchUp": {"paramNames": [], "type": "component_event"}, # new
    "EmailPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "EmailPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "EmailPicker.RequestFocus": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.GetBatteryCurrent": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.GetBatteryVoltage": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.GetFirmwareBuild": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.GetFirmwareVersion": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.GetHardwardVersion": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.GetOSBuild": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.GetOSVersion": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Commands.KeepAlive": {"kind": "statement", "paramNames": ["minutes"], "type": "component_method"}, # new
    "Ev3ColorSensor.AboveRange": {"paramNames": [], "type": "component_event"}, # new
    "Ev3ColorSensor.BelowRange": {"paramNames": [], "type": "component_event"}, # new
    "Ev3ColorSensor.ColorChanged": {"paramNames": ["colorCode","colorName"], "type": "component_event"}, # new
    "Ev3ColorSensor.GetColorCode": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3ColorSensor.GetColorName": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3ColorSensor.GetLightLevel": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3ColorSensor.SetAmbientMode": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3ColorSensor.SetColorMode": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3ColorSensor.SetReflectedMode": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3ColorSensor.WithinRange": {"paramNames": [], "type": "component_event"}, # new
    "Ev3GyroSensor.GetColorCode": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3GyroSensor.SensorValueChanged": {"paramNames": ["sensorValue"], "type": "component_event"}, # new
    "Ev3GyroSensor.SetAngleMode": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3GyroSensor.SetRateMode": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3Motors.GetTachoCount": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3Motors.ResetTachoCount": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3Motors.RotateInDistance": {"kind": "statement", "paramNames": ["power","distance","useBrake"], "type": "component_method"}, # new
    "Ev3Motors.RotateInDuration": {"kind": "statement", "paramNames": ["power","milliseconds","useBrake"], "type": "component_method"}, # new
    "Ev3Motors.RotateInTachoCounts": {"kind": "statement", "paramNames": ["power","tachoCounts","useBrake"], "type": "component_method"}, # new
    "Ev3Motors.RotateIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"}, # new
    "Ev3Motors.RotateSyncInDistance": {"kind": "statement", "paramNames": ["power","distance","turnRatio","useBrake"], "type": "component_method"}, # new
    "Ev3Motors.RotateSyncInDuration": {"kind": "statement", "paramNames": ["power","milliseconds","turnRatio","useBrake"], "type": "component_method"}, # new
    "Ev3Motors.RotateSyncInTachoCounts": {"kind": "statement", "paramNames": ["power","tachoCounts","turnRatio","useBrake"], "type": "component_method"}, # new
    "Ev3Motors.RotateSyncIndefinitely": {"kind": "statement", "paramNames": ["power","turnRatio"], "type": "component_method"}, # new
    "Ev3Motors.Stop": {"kind": "statement", "paramNames": ["useBrake"], "type": "component_method"}, # new
    "Ev3Motors.TachoCount": {"paramNames": ["tachoCount"], "type": "component_event"}, # new
    "Ev3Motors.ToggleDirection": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3Sound.PlayTone": {"kind": "statement", "paramNames": ["volume", "frequency", "milliseconds"], "type": "component_method"}, # new
    "Ev3Sound.StopSound": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3TouchSensor.IsPressed": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3TouchSensor.Pressed": {"paramNames": [], "type": "component_event"}, # new
    "Ev3TouchSensor.Released": {"paramNames": [], "type": "component_event"}, # new
    "Ev3UI.DrawCircle": {"kind": "statement", "paramNames": ["color","x","y","radius","fill"], "type": "component_method"}, # new
    "Ev3UI.DrawIcon": {"kind": "statement", "paramNames": ["color","x","y","type","no"], "type": "component_method"}, # new
    "Ev3UI.DrawLine": {"kind": "statement", "paramNames": ["color","x1","y1","x2","y2"], "type": "component_method"}, # new
    "Ev3UI.DrawPoint": {"kind": "statement", "paramNames": ["color","x","y"], "type": "component_method"}, # new
    "Ev3UI.DrawRect": {"kind": "statement", "paramNames": ["color","x","y","width","height","fill"], "type": "component_method"}, # new
    "Ev3UI.FillScreen": {"kind": "statement", "paramNames": ["color"], "type": "component_method"}, # new
    "Ev3UltrasonicSensor.AboveRange": {"paramNames": [], "type": "component_event"}, # new
    "Ev3UltrasonicSensor.BelowRange": {"paramNames": [], "type": "component_event"}, # new
    "Ev3UltrasonicSensor.GetDistance": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "Ev3UltrasonicSensor.SetCmUnit": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3UltrasonicSensor.SetInchUnit": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Ev3UlstrasonicSensor.WithinRange": {"paramNames": [], "type": "component_event"}, # new
    "File.AfterFileSaved": {"paramNames": ["fileName"], "type": "component_event"}, # new
    "File.AppendToFile": {"kind": "statement", "paramNames": ["text","fileName"], "type": "component_method"}, # new
    "File.Delete": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"}, # new
    "File.GotText": {"paramNames": ["text"], "type": "component_event"}, # new
    "File.ReadFrom": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"}, # new
    "File.SaveFile": {"kind": "statement", "paramNames": ["text","fileName"], "type": "component_method"}, # new
    "FirebaseDB.AppendValue": {"kind": "statement", "paramNames": ["tag","valueToAdd"], "type": "component_method"}, # new
    "FirebaseDB.ClearTag": {"kind": "statement", "paramNames": ["tag"], "type": "component_method"}, # new
    "FirebaseDB.DataChanged": {"paramNames": ["tag","value"], "type": "component_event"}, # new
    "FirebaseDB.FirebaseError": {"paramNames": ["message"], "type": "component_event"}, # new
    "FirebaseDB.FirstRemoved": {"paramNames": ["value"], "type": "component_event"}, # new
    "FirebaseDB.GotValue": {"paramNames": ["tag","value"], "type": "component_event"}, # new
    "FirebaseDB.GetTagList": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "FirebaseDB.GetValue": {"kind": "statement", "paramNames": ["tag", "valueIfTagNotThere"], "type": "component_method"}, # new
    "FirebaseDB.RemoveFirst": {"kind": "statement", "paramNames": ["tag"], "type": "component_method"}, # new
    "FirebaseDB.StoreValue": {"kind": "statement", "paramNames": ["tag", "valueToStore"], "type": "component_method"}, # new
    "FirebaseDB.TagList": {"paramNames": ["value"], "type": "component_event"}, # new
    "FirebaseDB.Unauthenticate": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    #"FusiontablesControl.DoQuery": {"kind": "statement", "paramNames": [], "type": "component_method"}, # removed?
    "FusiontablesControl.ForgetLogin": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "FusiontablesControl.GotResult": {"paramNames": ["result"], "type": "component_event"},
    "FusiontablesControl.GetRows": {"kind": "statement", "paramNames": ["tableId","columns"], "type": "component_method"}, # new
    "FusiontablesControl.GetRowsWithConditions": {"kind": "statement", "paramNames": ["tableId","columns","conditions"], "type": "component_method"}, # new
    "FusiontablesControl.InsertRow": {"kind": "statement", "paramNames": ["tableId","columns","values"], "type": "component_method"}, # new
    "FusiontablesControl.SendQuery": {"kind": "statement", "paramNames": [], "type": "component_method"},
    # [2017/03/28] I can't find GameClient in version nb155, but I'll keep it anyway
    "GameClient.FunctionCompleted": {"paramNames": ["functionName"], "type": "component_event"},
    "GameClient.GetInstanceLists": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.GetMessages": {"kind": "statement", "paramNames": ["type", "count"], "type": "component_method"},
    "GameClient.GotMessage": {"paramNames": ["type", "sender", "contents"], "type": "component_event"},
    "GameClient.Info": {"paramNames": ["message"], "type": "component_event"},
    "GameClient.InstanceIdChanged": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.Invite": {"kind": "statement", "paramNames": ["playerEmail"], "type": "component_method"},
    "GameClient.Invited": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.LeaveInstance": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "GameClient.MakeNewInstance": {"kind": "statement", "paramNames": ["instanceId", "makePublic"], "type": "component_method"},
    "GameClient.NewInstanceMade": {"paramNames": ["instanceId"], "type": "component_event"},
    "GameClient.NewLeader": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.PlayerJoined": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.PlayerLeft": {"paramNames": ["playerId"], "type": "component_event"},
    "GameClient.SendMessage": {"kind": "statement", "paramNames": ["type", "recipients", "contents"], "type": "component_method"},
    "GameClient.ServerCommand": {"kind": "statement", "paramNames": ["command", "arguments"], "type": "component_method"},
    "GameClient.ServerCommandFailure": {"paramNames": ["command", "arguments"], "type": "component_event"},
    "GameClient.ServerCommandSuccess": {"paramNames": ["command", "response"], "type": "component_event"},
    "GameClient.SetInstance": {"kind": "statement", "paramNames": ["instanceId"], "type": "component_method"},
    "GameClient.SetLeader": {"kind": "statement", "paramNames": ["playerEmail"], "type": "component_method"},
    "GameClient.UserEmailAddressSet": {"paramNames": ["emailAddress"], "type": "component_event"},
    "GameClient.WebServiceError": {"paramNames": ["functionName", "message"], "type": "component_event"},
    "GyroscopeSensor.GyroscopeChanged": {"paramNames": ["xAngularVelocity","yAngularVelocity","zAngularVelocity","timestamp"], "type": "component_event"}, # new
    "ImagePicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ImagePicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ImagePicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ImagePicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ImagePicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "ImagePicker.TouchDown": {"paramNames": [], "type": "component_event"}, # new
    "ImagePicker.TouchUp": {"paramNames": [], "type": "component_event"}, # new
    "ImageSprite.Bounce": {"kind": "statement", "paramNames": ["edge"], "type": "component_method"},
    "ImageSprite.CollidedWith": {"paramNames": ["other"], "type": "component_event"},
    "ImageSprite.CollidingWith": {"kind": "expression", "paramNames": ["other"], "type": "component_method"},
    "ImageSprite.Dragged": {"paramNames": ["startX", "startY", "prevX", "prevY", "currentX", "currentY"], "type": "component_event"},
    "ImageSprite.EdgeReached": {"paramNames": ["edge"], "type": "component_event"},
    "ImageSprite.Flung": {"paramNames": ["x", "y", "speed", "heading", "xvel", "yvel"], "type": "component_event"},
    "ImageSprite.MoveIntoBounds": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "ImageSprite.MoveTo": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "ImageSprite.NoLongerCollidingWith": {"paramNames": ["other"], "type": "component_event"},
    "ImageSprite.PointInDirection": {"kind": "statement", "paramNames": ["x", "y"], "type": "component_method"},
    "ImageSprite.PointTowards": {"kind": "statement", "paramNames": ["target"], "type": "component_method"},
    "ImageSprite.TouchDown": {"paramNames": ["x", "y"], "type": "component_event"},
    "ImageSprite.TouchUp": {"paramNames": ["x", "y"], "type": "component_event"},
    "ImageSprite.Touched": {"paramNames": ["x", "y"], "type": "component_event"},
    "ListPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "ListPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "ListPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "ListPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "ListPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "ListPicker.TouchDown": {"paramNames": [], "type": "component_event"}, # new
    "ListPicker.TouchUp": {"paramNames": [], "type": "component_event"}, # new
    "ListView.AfterPicking": {"paramNames": [], "type": "component_event"}, # new
    "LocationSensor.LatitudeFromAddress": {"kind": "expression", "paramNames": ["locationName"], "type": "component_method"},
    "LocationSensor.LocationChanged": {"paramNames": ["latitude", "longitude", "altitude","speed"], "type": "component_event"}, # new
    "LocationSensor.LongitudeFromAddress": {"kind": "expression", "paramNames": ["locationName"], "type": "component_method"},
    "LocationSensor.StatusChanged": {"paramNames": ["provider", "status"], "type": "component_event"},
    "NearField.TagRead": {"paramNames": ["message"], "type": "component_event"},
    "NearField.TagWritten": {"paramNames": [], "type": "component_event"},
    "Notifier.AfterChoosing": {"paramNames": ["choice"], "type": "component_event"},
    "Notifier.AfterTextInput": {"paramNames": ["response"], "type": "component_event"},
    "Notifier.DismissProgressDialog": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "Notifier.LogError": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.LogInfo": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.LogWarning": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Notifier.ShowAlert": {"kind": "statement", "paramNames": ["notice"], "type": "component_method"},
    "Notifier.ShowChooseDialog": {"kind": "statement", "paramNames": ["message", "title", "button1Text", "button2Text", "cancelable"], "type": "component_method"},
    "Notifier.ShowMessageDialog": {"kind": "statement", "paramNames": ["message", "title", "buttonText"], "type": "component_method"},
    "Notifier.ShowProgressDialog": {"kind": "statement", "paramNames": ["message", "title"], "type": "component_method"}, # new
    "Notifier.ShowTextDialog": {"kind": "statement", "paramNames": ["message", "title", "cancelable"], "type": "component_method"},
    "NxtColorSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtColorSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtColorSensor.ColorChanged": {"paramNames": ["color"], "type": "component_event"},
    "NxtColorSensor.GetColor": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtColorSensor.GetLightLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtColorSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtDirectCommands.DeleteFile": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"},
    "NxtDirectCommands.DownloadFile": {"kind": "statement", "paramNames": ["source", "destination"], "type": "component_method"},
    "NxtDirectCommands.GetBatteryLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetBrickName": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetCurrentProgramName": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetFirmwareVersion": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.GetInputValues": {"kind": "expression", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.GetOutputState": {"kind": "expression", "paramNames": ["motorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.KeepAlive": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.ListFiles": {"kind": "expression", "paramNames": ["wildcard"], "type": "component_method"},
    "NxtDirectCommands.LsGetStatus": {"kind": "expression", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.LsRead": {"kind": "expression", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.LsWrite": {"kind": "statement", "paramNames": ["sensorPortLetter", "list", "rxDataLength"], "type": "component_method"},
    "NxtDirectCommands.MessageRead": {"kind": "expression", "paramNames": ["mailbox"], "type": "component_method"},
    "NxtDirectCommands.MessageWrite": {"kind": "statement", "paramNames": ["mailbox", "message"], "type": "component_method"},
    "NxtDirectCommands.PlaySoundFile": {"kind": "statement", "paramNames": ["fileName"], "type": "component_method"},
    "NxtDirectCommands.PlayTone": {"kind": "statement", "paramNames": ["frequencyHz", "durationMs"], "type": "component_method"},
    "NxtDirectCommands.ResetInputScaledValue": {"kind": "statement", "paramNames": ["sensorPortLetter"], "type": "component_method"},
    "NxtDirectCommands.ResetMotorPosition": {"kind": "statement", "paramNames": ["motorPortLetter", "relative"], "type": "component_method"},
    "NxtDirectCommands.SetBrickName": {"kind": "statement", "paramNames": ["name"], "type": "component_method"},
    "NxtDirectCommands.SetInputMode": {"kind": "statement", "paramNames": ["sensorPortLetter", "sensorType", "sensorMode"], "type": "component_method"},
    "NxtDirectCommands.SetOutputState": {"kind": "statement", "paramNames": ["motorPortLetter", "power", "mode", "regulationMode", "turnRatio", "runState", "tachoLimit"], "type": "component_method"},
    "NxtDirectCommands.StartProgram": {"kind": "statement", "paramNames": ["programName"], "type": "component_method"},
    "NxtDirectCommands.StopProgram": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDirectCommands.StopSoundPlayback": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDrive.MoveBackward": {"kind": "statement", "paramNames": ["power", "distance"], "type": "component_method"},
    "NxtDrive.MoveBackwardIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.MoveForward": {"kind": "statement", "paramNames": ["power", "distance"], "type": "component_method"},
    "NxtDrive.MoveForwardIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "NxtDrive.TurnClockwiseIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtDrive.TurnCounterClockwiseIndefinitely": {"kind": "statement", "paramNames": ["power"], "type": "component_method"},
    "NxtLightSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtLightSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtLightSensor.GetLightLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtLightSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtSoundSensor.GetSoundLevel": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtSoundSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "NxtTouchSensor.IsPressed": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtTouchSensor.Pressed": {"paramNames": [], "type": "component_event"},
    "NxtTouchSensor.Released": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.AboveRange": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.BelowRange": {"paramNames": [], "type": "component_event"},
    "NxtUltrasonicSensor.GetDistance": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "NxtUltrasonicSensor.WithinRange": {"paramNames": [], "type": "component_event"},
    "OrientationSensor.OrientationChanged": {"paramNames": ["azimuth", "pitch", "roll"], "type": "component_event"},
    "PasswordTextBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "PasswordTextBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "PasswordTextBox.RequestFocus": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    # "Pedometer.CalibrationFailed": {"paramNames": [], "type": "component_event"}, # removed
    # "Pedometer.GPSAvailable": {"paramNames": [], "type": "component_event"}, # removed
    # "Pedometer.GPSLost": {"paramNames": [], "type": "component_event"}, # removed
    "Pedometer.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Reset": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Resume": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.Save": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.SimpleStep": {"paramNames": ["simpleSteps", "distance"], "type": "component_event"},
    "Pedometer.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    # "Pedometer.StartedMoving": {"paramNames": [], "type": "component_event"}, # removed
    "Pedometer.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Pedometer.StoppedMoving": {"paramNames": [], "type": "component_event"},
    "Pedometer.WalkStep": {"paramNames": ["walkSteps", "distance"], "type": "component_event"},
    "PhoneCall.IncomingCallAnswered": {"paramNames": ["phoneNumber"], "type": "component_event"}, # new
    "PhoneCall.MakePhoneCall": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "PhoneCall.PhoneCallEnded": {"paramNames": ["status", "phoneNumber"], "type": "component_event"}, # new
    "PhoneCall.PhoneCallStarted": {"paramNames": ["status", "phoneNumber"], "type": "component_event"}, # new
    "PhoneNumberPicker.AfterPicking": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.BeforePicking": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.GotFocus": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.LostFocus": {"paramNames": [], "type": "component_event"},
    "PhoneNumberPicker.Open": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "PhoneNumberPicker.TouchDown": {"paramNames": [], "type": "component_event"}, # new
    "PhoneNumberPicker.TouchUp": {"paramNames": [], "type": "component_event"}, # new
    "PhoneNumberPicker.ViewContact": {"kind": "statement", "paramNames": ["uri"], "type": "component_method"}, # new
    "PhoneStatus.GetWifiIpAddress": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "PhoneStatus.isConnected": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "Player.Completed": {"paramNames": [], "type": "component_event"},
    "Player.OtherPlayerStarted": {"paramNames": [], "type": "component_event"}, # new
    "Player.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.PlayerError": {"paramNames": ["message"], "type": "component_event"},
    "Player.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Player.Vibrate": {"kind": "statement", "paramNames": ["milliseconds"], "type": "component_method"},
    "ProximitySensor.ProximityChanged": {"kind": "statement", "paramNames": ["distance"], "type": "component_method"}, # new
    "Screen.BackPressed": {"paramNames": [], "type": "component_event"},
    # "Screen.CloseScreenAnimation": {"kind": "statement", "paramNames": ["animType"], "type": "component_method"}, # removed
    "Screen.ErrorOccurred": {"paramNames": ["component", "functionName", "errorNumber", "message"], "type": "component_event"},
    "Screen.HideKeyboard": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new 
    "Screen.Initialize": {"paramNames": [], "type": "component_event"},
    # "Screen.OpenScreenAnimation": {"kind": "statement", "paramNames": ["animType"], "type": "component_method"}, # removed
    "Screen.OtherScreenClosed": {"paramNames": ["otherScreenName", "result"], "type": "component_event"},
    "Screen.ScreenOrientationChanged": {"paramNames": [], "type": "component_event"},
    "Sharing.ShareFile": {"kind": "statement", "paramNames": ["file"], "type": "component_method"}, # new
    "Sharing.ShareFileWithMessage": {"kind": "statement", "paramNames": ["file", "message"], "type": "component_method"}, # new
    "Sharing.ShareMessage": {"kind": "statement", "paramNames": ["message"], "type": "component_method"}, # new
    "Slider.PositionChanged": {"paramNames": ["thumbPosition"], "type": "component_event"}, # new
    "Sound.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Play": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Resume": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.SoundError": {"paramNames": ["message"], "type": "component_event"},
    "Sound.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Sound.Vibrate": {"kind": "statement", "paramNames": ["millisecs"], "type": "component_method"},
    "SoundRecorder.AfterSoundRecorded": {"paramNames": ["sound"], "type": "component_event"},
    "SoundRecorder.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "SoundRecorder.StartedRecording": {"paramNames": [], "type": "component_event"},
    "SoundRecorder.Stop": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "SoundRecorder.StoppedRecording": {"paramNames": [], "type": "component_event"},
    "SpeechRecognizer.AfterGettingText": {"paramNames": ["result"], "type": "component_event"},
    "SpeechRecognizer.BeforeGettingText": {"paramNames": [], "type": "component_event"},
    "SpeechRecognizer.GetText": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Spinner.AfterSelecting": {"paramNames": ["selection"], "type": "component_event"}, # new
    "Spinner.DisplayDropdown": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "TextBox.GotFocus": {"paramNames": [], "type": "component_event"},
    "TextBox.HideKeyboard": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TextBox.RequestFocus": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "TextBox.LostFocus": {"paramNames": [], "type": "component_event"},
    "TextToSpeech.AfterSpeaking": {"paramNames": ["result"], "type": "component_event"},
    "TextToSpeech.BeforeSpeaking": {"paramNames": [], "type": "component_event"},
    "TextToSpeech.Speak": {"kind": "statement", "paramNames": ["message"], "type": "component_method"},
    "Texting.MessageReceived": {"paramNames": ["number", "messageText"], "type": "component_event"},
    "Texting.SendMessage": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "TimePicker.AfterTimeSet": {"paramNames": [], "type": "component_event"}, # new
    "TimePicker.GotFocus": {"paramNames": [], "type": "component_event"}, # new
    "TimePicker.LaunchPicker": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "TimePicker.LostFocus": {"paramNames": [], "type": "component_event"}, # new
    "TimePicker.SetTimeToDisplay": {"kind": "statement", "paramNames": ["hour","minute"], "type": "component_method"}, # new
    "TimePicker.SetTimeToDisplayFromInstant": {"kind": "statement", "paramNames": ["instant"], "type": "component_method"}, # new
    "TimePicker.TouchDown": {"paramNames": [], "type": "component_event"}, # new
    "TimePicker.TouchUp": {"paramNames": [], "type": "component_event"}, # new
    "TinyDB.ClearAll": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "TinyDB.ClearTag": {"kind": "statement", "paramNames": ["tag"], "type": "component_method"}, # new
    "TinyDB.GetTags": {"kind": "expression", "paramNames": [], "type": "component_method"}, # new
    "TinyDB.GetValue": {"kind": "expression", "paramNames": ["tag","valueIfTagNotThere"], "type": "component_method"}, # new 2nd param
    "TinyDB.StoreValue": {"kind": "statement", "paramNames": ["tag", "valueToStore"], "type": "component_method"},
    "TinyWebDB.GetValue": {"kind": "statement", "paramNames": ["tag"], "type": "component_method"},
    "TinyWebDB.GotValue": {"paramNames": ["tagFromWebDB", "valueFromWebDB"], "type": "component_event"},
    "TinyWebDB.StoreValue": {"kind": "statement", "paramNames": ["tag", "valueToStore"], "type": "component_method"},
    "TinyWebDB.ValueStored": {"paramNames": [], "type": "component_event"},
    "TinyWebDB.WebServiceError": {"paramNames": ["message"], "type": "component_event"},
    "Twitter.Authorize": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.CheckAuthorized": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.DeAuthorize": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.DirectMessage": {"kind": "statement", "paramNames": ["user", "message"], "type": "component_method"},
    "Twitter.DirectMessagesReceived": {"paramNames": ["messages"], "type": "component_event"},
    "Twitter.Follow": {"kind": "statement", "paramNames": ["user"], "type": "component_method"},
    "Twitter.FollowersReceived": {"paramNames": ["followers2"], "type": "component_event"},
    "Twitter.FriendTimelineReceived": {"paramNames": ["timeline"], "type": "component_event"},
    "Twitter.IsAuthorized": {"paramNames": [], "type": "component_event"},
    "Twitter.Login": {"kind": "statement", "paramNames": ["username", "password"], "type": "component_method"},
    "Twitter.MentionsReceived": {"paramNames": ["mentions"], "type": "component_event"},
    "Twitter.RequestDirectMessages": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestFollowers": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestFriendTimeline": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.RequestMentions": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Twitter.SearchSuccessful": {"paramNames": ["searchResults"], "type": "component_event"},
    "Twitter.SearchTwitter": {"kind": "statement", "paramNames": ["query"], "type": "component_method"},
    # "Twitter.SetStatus": {"kind": "statement", "paramNames": ["status"], "type": "component_method"}, # removed
    "Twitter.StopFollowing": {"kind": "statement", "paramNames": ["user"], "type": "component_method"},
    "Twitter.Tweet": {"kind": "statement", "paramNames": ["status"], "type": "component_method"}, # new
    "Twitter.TweetWithImage": {"kind": "statement", "paramNames": ["status","imagePath"], "type": "component_method"}, # new
    "VideoPlayer.Completed": {"paramNames": [], "type": "component_event"},
    "VideoPlayer.GetDuration": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "VideoPlayer.Pause": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "VideoPlayer.SeekTo": {"kind": "statement", "paramNames": ["ms"], "type": "component_method"},
    "VideoPlayer.Start": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "VideoPlayer.VideoPlayerError": {"paramNames": ["message"], "type": "component_event"},
    # [2017/03/28] I can't find Voting in version nb155, but I'll keep it anyway
    "Voting.GotBallot": {"paramNames": [], "type": "component_event"},
    "Voting.GotBallotConfirmation": {"paramNames": [], "type": "component_event"},
    "Voting.NoOpenPoll": {"paramNames": [], "type": "component_event"},
    "Voting.RequestBallot": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Voting.SendBallot": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Voting.WebServiceError": {"paramNames": ["message"], "type": "component_event"},
    "Web.BuildRequestData": {"kind": "expression", "paramNames": ["list"], "type": "component_method"},
    "Web.ClearCookies": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.Delete": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.Get": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "Web.GotFile": {"paramNames": ["url", "responseCode", "responseType", "fileName"], "type": "component_event"},
    "Web.GotText": {"paramNames": ["url", "responseCode", "responseType", "responseContent"], "type": "component_event"},
    "Web.HtmlTextDecode": {"kind": "expression", "paramNames": ["htmlText"], "type": "component_method"},
    "Web.JsonTextDecode": {"kind": "expression", "paramNames": ["jsonText"], "type": "component_method"},
    "Web.PostFile": {"kind": "statement", "paramNames": ["path"], "type": "component_method"},
    "Web.PostText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "Web.PostTextWithEncoding": {"kind": "statement", "paramNames": ["text", "encoding"], "type": "component_method"},
    "Web.PutFile": {"kind": "statement", "paramNames": ["path"], "type": "component_method"},
    "Web.PutText": {"kind": "statement", "paramNames": ["text"], "type": "component_method"},
    "Web.PutTextWithEncoding": {"kind": "statement", "paramNames": ["text", "encoding"], "type": "component_method"},
    "Web.UriEncode": {"kind": "expression", "paramNames": ["text"], "type": "component_method"},
    "Web.XMLTextDecode": {"kind": "expression", "paramNames": ["XmlText"], "type": "component_method"}, # new
    "WebViewer.CanGoBack": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "WebViewer.CanGoForward": {"kind": "expression", "paramNames": [], "type": "component_method"},
    "WebViewer.ClearCaches": {"kind": "statement", "paramNames": [], "type": "component_method"}, # new
    "WebViewer.ClearLocations": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoBack": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoForward": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoHome": {"kind": "statement", "paramNames": [], "type": "component_method"},
    "WebViewer.GoToUrl": {"kind": "statement", "paramNames": ["url"], "type": "component_method"},
    "YandexTranslate.GotTranslation": {"kind": "statement", "paramNames": ["responseCode","translation"], "type": "component_method"}, # new
    "YandexTranslate.RequestTranslation": {"kind": "statement", "paramNames": ["languageToTranslateTo","textToTranslate"], "type": "component_method"} # new
}

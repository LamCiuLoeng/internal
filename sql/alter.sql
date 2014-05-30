ALTER TABLE sample_sub_form_avon ALTER COLUMN quantity_pcs TYPE character varying(500);
ALTER TABLE orchestra_order ALTER COLUMN quantity_pcs TYPE character varying(500);

alter table sample_sub_form_sampling ADD COLUMN file_from_task_name  CHARACTER VARYING(100);
alter table sample_sub_form_printout add COLUMN file_from_task_name  CHARACTER VARYING(100);

=A6&"'"&TRIM(B6)&"','"&TRIM(C6)&"',"&"'"&TRIM(D6)&"',"&"'"&TRIM(E6)&"');"
=A121&"'"&TRIM(B121)&"','"&TRIM(C121)&"',"&"'"&TRIM(D121)&"',"&"'"&TRIM(E121)&"',"&"'"&TRIM(F121)&"',"&"'"&TRIM(G121)&"',"&"'"&TRIM(H121)&"',"&"'"&TRIM(I121)&"',"&"'"&TRIM(J121)&"');"

alter table sample_main_form alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_3dimage alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_artwork alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_assembly alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_avon alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_bestbuy alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_box alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_container alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_drop_test alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_file_convert alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_floor alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_general alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_label alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_photo alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_printout alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_sampling alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_target alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_tray alter column attachment type CHARACTER VARYING(999);
alter table sample_sub_form_upload alter column attachment type CHARACTER VARYING(999);

alter table sample_main_form alter column reference_code type TEXT;
alter table sample_main_form alter column item_description type TEXT;
alter table sample_main_form alter column item_code type TEXT;
alter table sample_main_form alter column child_form type TEXT;
alter table sample_main_form alter column request_contact_number type TEXT;
alter table sample_main_form alter column cc_to type TEXT;

alter table sample_sub_form_target alter column dept_id type Text;
alter table sample_sub_form_target alter column promo_id type Text;
alter table sample_sub_form_target alter column dpci type Text;
alter table sample_sub_form_target alter column packaging_style type Text;
alter table sample_sub_form_target alter column vendor_style type Text;
alter table sample_sub_form_target alter column spg type Text;
alter table sample_sub_form_target alter column dimension type Text;
alter table sample_sub_form_target alter column insert type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column material type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column submitted_item type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column submitted_item_other type Text;
alter table sample_sub_form_target alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column file_from_ftp_location type Text;
alter table sample_sub_form_target alter column file_from_files_location type Text;
alter table sample_sub_form_target add column factory_code CHARACTER VARYING(99);
alter table sample_sub_form_target alter column factory_code type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column size_w type Text;
alter table sample_sub_form_target alter column size_h type Text;
alter table sample_sub_form_target alter column size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column color type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column color_spot_content type Text;
alter table sample_sub_form_target alter column color_other_content type Text;
alter table sample_sub_form_target alter column die type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column file_format type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column target_format type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column file_protection type CHARACTER VARYING(99);
alter table sample_sub_form_target alter column remark type Text;

alter table sample_sub_form_avon alter column pp_no type TEXT;
alter table sample_sub_form_avon alter column category type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column sample type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column artwork type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column dimension_type type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column product_width type TEXT;
alter table sample_sub_form_avon alter column product_depth type TEXT;
alter table sample_sub_form_avon alter column product_height type TEXT;
alter table sample_sub_form_avon alter column product_unit type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column product_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column dimension_width type TEXT;
alter table sample_sub_form_avon alter column dimension_depth type TEXT;
alter table sample_sub_form_avon alter column dimension_height type TEXT;
alter table sample_sub_form_avon alter column dimension_unit type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column dimension_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column box_width type TEXT;
alter table sample_sub_form_avon alter column box_depth type TEXT;
alter table sample_sub_form_avon alter column box_height type TEXT;
alter table sample_sub_form_avon alter column box_unit type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column box_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column box_size type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column product_weight type TEXT;
alter table sample_sub_form_avon alter column product_weight_unit type CHARACTER VARYING(49);
alter table sample_sub_form_avon alter column product_weight_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column top type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column top_other type TEXT;
alter table sample_sub_form_avon alter column mp_width type TEXT;
alter table sample_sub_form_avon alter column mp_depth type TEXT;
alter table sample_sub_form_avon alter column mp_height type TEXT;
alter table sample_sub_form_avon alter column mp_unit type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column mp_size type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column quantity type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column quantity_pcs type TEXT;
alter table sample_sub_form_avon alter column country type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column country_other type TEXT;
alter table sample_sub_form_avon alter column product type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column design_criteria type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column artwork_file_from type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column artwork_file_from_ftp_location type TEXT;
alter table sample_sub_form_avon alter column artwork_file_from_files_location type TEXT;
alter table sample_sub_form_avon alter column artwork_factory_code type CHARACTER VARYING(49);
alter table sample_sub_form_avon alter column artwork_size_w type TEXT;
alter table sample_sub_form_avon alter column artwork_size_h type TEXT;
alter table sample_sub_form_avon alter column artwork_size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column artwork_color type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column artwork_color_spot_content type TEXT;
alter table sample_sub_form_avon alter column artwork_color_other_content type TEXT;
alter table sample_sub_form_avon alter column artwork_output type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column artwork_protection type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column artwork_output_other_content type TEXT;
alter table sample_sub_form_avon alter column label_size_w type TEXT;
alter table sample_sub_form_avon alter column label_size_h type TEXT;
alter table sample_sub_form_avon alter column label_size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column label_material type TEXT;
alter table sample_sub_form_avon alter column label_country type TEXT;
alter table sample_sub_form_avon alter column label_item_code type TEXT;
alter table sample_sub_form_avon alter column label_item_name type TEXT;
alter table sample_sub_form_avon alter column label_barcode type CHARACTER VARYING(49);
alter table sample_sub_form_avon alter column label_font type TEXT;
alter table sample_sub_form_avon alter column label_content_color type TEXT;
alter table sample_sub_form_avon alter column label_color type CHARACTER VARYING(99);
alter table sample_sub_form_avon alter column label_color_other type TEXT;
alter table sample_sub_form_avon alter column requirement type TEXT;

alter table sample_sub_form_bestbuy alter column job_purpose type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column job_presentation type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column submit_items type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column submit_items_other type Text;
alter table sample_sub_form_bestbuy alter column size_w type Text;
alter table sample_sub_form_bestbuy alter column size_d type Text;
alter table sample_sub_form_bestbuy alter column size_h type Text;
alter table sample_sub_form_bestbuy alter column size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column size_type type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column size_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column weight type Text;
alter table sample_sub_form_bestbuy alter column weight_unit type CHARACTER VARYING(49);
alter table sample_sub_form_bestbuy alter column weight_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column material_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column material_type type CHARACTER VARYING(999);
alter table sample_sub_form_bestbuy alter column window_size_w type Text;
alter table sample_sub_form_bestbuy alter column window_size_d type Text;
alter table sample_sub_form_bestbuy alter column window_size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column material_other type Text;
alter table sample_sub_form_bestbuy alter column requirement type CHARACTER VARYING(99);
alter table sample_sub_form_bestbuy alter column remark type Text;

alter table sample_sub_form_box alter column job_perpose type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column presentation type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column product_or_box type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column product_w type Text;
alter table sample_sub_form_box alter column product_d type Text;
alter table sample_sub_form_box alter column product_h type Text;
alter table sample_sub_form_box alter column product_unit type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column product_weight type Text;
alter table sample_sub_form_box alter column product_weight_unit type CHARACTER VARYING(49);
alter table sample_sub_form_box alter column box_w type Text;
alter table sample_sub_form_box alter column box_d type Text;
alter table sample_sub_form_box alter column box_h type Text;
alter table sample_sub_form_box alter column box_unit type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column box_size type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column top_closure type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column top_closure_other type Text;
alter table sample_sub_form_box alter column top_locking type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column top_locking_other type Text;
alter table sample_sub_form_box alter column bottom_closure type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column bottom_closure_other type Text;
alter table sample_sub_form_box alter column bottom_locking type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column bottom_locking_other type Text;
alter table sample_sub_form_box alter column insert type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column loading type CHARACTER VARYING(99);
alter table sample_sub_form_box rename column "window" to window_type;
alter table sample_sub_form_box alter column window_type type CHARACTER VARYING(99)
alter table sample_sub_form_box alter column window_with type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column pvc_thickness type Text;
alter table sample_sub_form_box alter column pet_thickness type Text;
alter table sample_sub_form_box alter column pp_thickness type Text;
alter table sample_sub_form_box alter column window_with_other_content type Text;
alter table sample_sub_form_box alter column window_with_other_unit type Text;
alter table sample_sub_form_box alter column window_size_w type Text;
alter table sample_sub_form_box alter column window_size_h type Text;
alter table sample_sub_form_box alter column window_size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column suggested_by_pd_team type CHARACTER VARYING(99);
alter table sample_sub_form_box alter column remark type Text;

alter table sample_sub_form_tray alter column job_purpose type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column presentation type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column product_dimension_type type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column product_dimension_w type TEXT;
alter table sample_sub_form_tray alter column product_dimension_d type TEXT;
alter table sample_sub_form_tray alter column product_dimension_h type TEXT;
alter table sample_sub_form_tray alter column product_dimension_unit type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column product_dimension_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column weight type TEXT;
alter table sample_sub_form_tray alter column weight_unit type CHARACTER VARYING(49);
alter table sample_sub_form_tray alter column product_weight_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column product_tray_size type CHARACTER VARYING(49);
alter table sample_sub_form_tray alter column tray_dimension_w type TEXT;
alter table sample_sub_form_tray alter column tray_dimension_d type TEXT;
alter table sample_sub_form_tray alter column tray_dimension_bh type TEXT;
alter table sample_sub_form_tray alter column tray_dimension_fh type TEXT;
alter table sample_sub_form_tray alter column tray_size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column box_size type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column tray_pack_left type TEXT;
alter table sample_sub_form_tray alter column tray_pack_front type TEXT;
alter table sample_sub_form_tray alter column tray_pack_top type TEXT;
alter table sample_sub_form_tray alter column stackable type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column style type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column tray_detail type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column tray_detail_hook_qty type TEXT;
alter table sample_sub_form_tray alter column tray_detail_thickness type TEXT;
alter table sample_sub_form_tray alter column tray_detail_thickness_unit type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column shipper type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column shipper_other_content type TEXT;
alter table sample_sub_form_tray alter column shipper_loading type CHARACTER VARYING(99);
alter table sample_sub_form_tray alter column remark type TEXT;

alter table sample_sub_form_floor alter column job_purpose type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column presentation type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column diagram_for_approval type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column dimension_type type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column dimension_w type Text;
alter table sample_sub_form_floor alter column dimension_d type Text;
alter table sample_sub_form_floor alter column dimension_h type Text;
alter table sample_sub_form_floor alter column dimension_unit type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column dimension_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column weight type Text;
alter table sample_sub_form_floor alter column weight_unit type CHARACTER VARYING(49);
alter table sample_sub_form_floor alter column weight_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column pallet_size type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column full_pallet type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column full_pallet_height_limit type Text;
alter table sample_sub_form_floor alter column full_pallet_height_limit_unit type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column half_pallet type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column half_pallet_height_limit type Text;
alter table sample_sub_form_floor alter column half_pallet_height_limit_unit type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column display_pack_left type Text;
alter table sample_sub_form_floor alter column display_pack_front type Text;
alter table sample_sub_form_floor alter column display_pack_top type Text;
alter table sample_sub_form_floor alter column other_size_w type Text;
alter table sample_sub_form_floor alter column other_size_d type Text;
alter table sample_sub_form_floor alter column other_size_h type Text;
alter table sample_sub_form_floor alter column other_size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column front_lip_height type Text;
alter table sample_sub_form_floor alter column front_lip_unit type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column shelves_left type Text;
alter table sample_sub_form_floor alter column shelves_top type Text;
alter table sample_sub_form_floor alter column pack_left type Text;
alter table sample_sub_form_floor alter column pack_front type Text;
alter table sample_sub_form_floor alter column top_to_bottom type Text;
alter table sample_sub_form_floor alter column style type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column facing type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column facing_other type Text;
alter table sample_sub_form_floor alter column detail_type type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column detail_height type Text;
alter table sample_sub_form_floor alter column detail_height_unit type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column detail_type_hook_qty type Text;
alter table sample_sub_form_floor alter column detail_type_other_content type Text;
alter table sample_sub_form_floor alter column shipper_type1 type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column shipper_type2 type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column transit type CHARACTER VARYING(99);
alter table sample_sub_form_floor alter column remark type Text;

alter table sample_sub_form_general alter column job_purpose type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column job_presentation type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column size_w type Text;
alter table sample_sub_form_general alter column size_d type Text;
alter table sample_sub_form_general alter column size_h type Text;
alter table sample_sub_form_general alter column size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column size_type type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column size_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column weight type Text;
alter table sample_sub_form_general alter column weight_unit type CHARACTER VARYING(49);
alter table sample_sub_form_general alter column weight_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column submit_item type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column submit_item_other type Text;
alter table sample_sub_form_general alter column item_type type CHARACTER VARYING(99);
alter table sample_sub_form_general alter column item_type_other type Text;
alter table sample_sub_form_general alter column remark type Text;

alter table sample_sub_form_label alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_label alter column file_from_ftp_location type Text;
alter table sample_sub_form_label alter column file_from_files_location type Text;
alter table sample_sub_form_label alter column size_w type Text;
alter table sample_sub_form_label alter column size_h type Text;
alter table sample_sub_form_label alter column size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_label alter column material type Text;
alter table sample_sub_form_label alter column country type Text;
alter table sample_sub_form_label alter column item_code type Text;
alter table sample_sub_form_label alter column item_name type Text;
alter table sample_sub_form_label alter column barcode type CHARACTER VARYING(49);
alter table sample_sub_form_label alter column font type Text;
alter table sample_sub_form_label alter column content_color type Text;
alter table sample_sub_form_label alter column color type CHARACTER VARYING(99);
alter table sample_sub_form_label alter column color_other type Text;
alter table sample_sub_form_label alter column output type CHARACTER VARYING(99);
alter table sample_sub_form_label alter column protection type CHARACTER VARYING(99);
alter table sample_sub_form_label alter column output_other_content type Text;
alter table sample_sub_form_label alter column remark type Text;

alter table sample_sub_form_artwork alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_artwork alter column file_from_ftp_location type Text;
alter table sample_sub_form_artwork alter column file_from_files_location type Text;
alter table sample_sub_form_artwork alter column factory_code type CHARACTER VARYING(49);
alter table sample_sub_form_artwork alter column size_w type Text;
alter table sample_sub_form_artwork alter column size_h type Text;
alter table sample_sub_form_artwork alter column size_unit type CHARACTER VARYING(99);
alter table sample_sub_form_artwork alter column color type CHARACTER VARYING(99);
alter table sample_sub_form_artwork alter column color_spot_content type Text;
alter table sample_sub_form_artwork alter column color_other_content type Text;
alter table sample_sub_form_artwork alter column output type CHARACTER VARYING(99);
alter table sample_sub_form_artwork alter column protection type CHARACTER VARYING(99);
alter table sample_sub_form_artwork alter column output_other_content type Text;
alter table sample_sub_form_artwork alter column remark type Text;

alter table sample_sub_form_sampling alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_sampling alter column file_from_ftp_location type TEXT;
alter table sample_sub_form_sampling alter column file_from_files_location type TEXT;
alter table sample_sub_form_sampling alter column file_from_task_name type TEXT;
alter table sample_sub_form_sampling alter column output type CHARACTER VARYING(99);
alter table sample_sub_form_sampling alter column output_white_pcs type INTEGER;
alter table sample_sub_form_sampling alter column output_woodfree_pcs type INTEGER;
alter table sample_sub_form_sampling alter column output_semi_pcs type INTEGER;
alter table sample_sub_form_sampling alter column output_label_pcs type INTEGER;
alter table sample_sub_form_sampling alter column delivery type CHARACTER VARYING(99);
alter table sample_sub_form_sampling alter column expected_time type CHARACTER VARYING(49);
alter table sample_sub_form_sampling alter column collection_point type CHARACTER VARYING(99);
alter table sample_sub_form_sampling alter column remark type TEXT;

alter table sample_sub_form_printout alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_printout alter column file_from_ftp_location type Text;
alter table sample_sub_form_printout alter column file_from_files_location type Text;
alter table sample_sub_form_printout alter column file_from_task_name type Text;
alter table sample_sub_form_printout alter column delivery type CHARACTER VARYING(99);
alter table sample_sub_form_printout alter column collection_point type CHARACTER VARYING(99);
alter table sample_sub_form_printout alter column expected_time type CHARACTER VARYING(49);
alter table sample_sub_form_printout alter column remark type Text;

alter table sample_sub_form_3dimage alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_3dimage alter column file_from_ftp_location type Text;
alter table sample_sub_form_3dimage alter column file_from_files_location type Text;
alter table sample_sub_form_3dimage alter column output type CHARACTER VARYING(99);
alter table sample_sub_form_3dimage alter column details type CHARACTER VARYING(99);
alter table sample_sub_form_3dimage alter column remark type Text;

alter table sample_sub_form_assembly alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_assembly alter column file_from_ftp_location type Text;
alter table sample_sub_form_assembly alter column file_from_files_location type Text;
alter table sample_sub_form_assembly alter column output type CHARACTER VARYING(99);
alter table sample_sub_form_assembly alter column remark type Text;

alter table sample_sub_form_drop_test alter column submit_items type CHARACTER VARYING(99);
alter table sample_sub_form_drop_test alter column submit_items_location type Text;
alter table sample_sub_form_drop_test alter column test_info type CHARACTER VARYING(99);
alter table sample_sub_form_drop_test alter column condition type CHARACTER VARYING(99);
alter table sample_sub_form_drop_test alter column condition_other_content type Text;
alter table sample_sub_form_drop_test alter column remark type Text;

alter table sample_sub_form_upload alter column checking type CHARACTER VARYING(99);
alter table sample_sub_form_upload alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_upload alter column from_ftp_location type TEXT;
alter table sample_sub_form_upload alter column from_public_location type TEXT;
alter table sample_sub_form_upload alter column file_to type CHARACTER VARYING(99);
alter table sample_sub_form_upload alter column to_ftp_location type TEXT;
alter table sample_sub_form_upload alter column to_public_location type TEXT;
alter table sample_sub_form_upload alter column remark type TEXT;

alter table sample_sub_form_container alter column weight type Text;
alter table sample_sub_form_container alter column weight_unit type CHARACTER VARYING(49);
alter table sample_sub_form_container alter column weight_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column size_according type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column outer_w type Text;
alter table sample_sub_form_container alter column outer_d type Text;
alter table sample_sub_form_container alter column outer_h type Text;
alter table sample_sub_form_container alter column outer_unit type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column outer_as_sample type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column pallet type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column pallet_w type Text;
alter table sample_sub_form_container alter column pallet_d type Text;
alter table sample_sub_form_container alter column pallet_h type Text;
alter table sample_sub_form_container alter column pallet_unit type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column orientation type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column info type CHARACTER VARYING(99);
alter table sample_sub_form_container alter column info_other type Text;
alter table sample_sub_form_container alter column remark type Text;

alter table sample_sub_form_file_convert alter column file_from type CHARACTER VARYING(99);
alter table sample_sub_form_file_convert alter column file_from_ftp_location type Text;
alter table sample_sub_form_file_convert alter column file_from_files_location type Text;
alter table sample_sub_form_file_convert alter column output type CHARACTER VARYING(99);
alter table sample_sub_form_file_convert alter column output_pdf_protection type CHARACTER VARYING(99);
alter table sample_sub_form_file_convert alter column output_other_content type Text;
alter table sample_sub_form_file_convert alter column remark type Text;

alter table sample_sub_form_photo alter column job_purpose type CHARACTER VARYING(99);
alter table sample_sub_form_photo alter column submit_items type CHARACTER VARYING(99);
alter table sample_sub_form_photo alter column submit_items_other type Text;
alter table sample_sub_form_photo alter column job_nature type CHARACTER VARYING(99);
alter table sample_sub_form_photo alter column output type CHARACTER VARYING(99);
alter table sample_sub_form_photo alter column output_other_content type Text;
alter table sample_sub_form_photo alter column remark type Text;

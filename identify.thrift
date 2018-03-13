service  FaceIdentify {
 void FI_add_face_database(1: string uid, 2: string user_info, 3: string group_id, 4: string imagename),
 i32 FI_del_face_database(1: string uid, 2: string group_id),
 i32 FI_update_face_database(1: string uid, 2: string user_info, 3: string group_id, 4: string imagename),
 i32 FI_find_user_info(1: string uid),
 string FI_find_group_users(1: string group_id),
 face_id_st FI_face_database_identify(1: string group_id, 2: string imagename),
 string FI_face_database_verify(1: string uid, 2: string user_info, 3: string group_id, 4: string imagename),
 i32 FI_group_deleteuser(1: string uid, 2: string group_id),
 i32 FI_group_adduser(1:string src_group_id, 2: string group_id, 3: string uid)
 face_detect_st FI_face_detect(1:string imagename)
 string FI_face_match(1:string image1, 2:string image2)  
}

struct rectangle {
	1:  i32 top;
  2:  i32 left;
  3:  i32 bottom;
  4:  i32 right;
}

/*A face info*/
struct face_info {
 1: string    uid;
 2: string    group;
 3: string    info;
 4: rectangle rect;
}

/*face identify return result*/
struct face_id_st{
 1: i32 result_num;
 2: map<i32,face_info> result;
}

/*detect face return result*/
struct face_detect_st {
 1: i32 result_num;
 2: map<i32,rectangle> result;
}

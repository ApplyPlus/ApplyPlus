diff --git a/net/rds/connection.c b/net/rds/connection.c
index 9b2de5e..49adeef 100644
--- a/net/rds/connection.c
+++ b/net/rds/connection.c
@@ -190,6 +190,12 @@ new_conn:
 		}
 	}
 
+	if (trans == NULL) {
+		kmem_cache_free(rds_conn_slab, conn);
+		conn = ERR_PTR(-ENODEV);
+		goto out;
+	}
+
 	conn->c_trans = trans;
 
 	ret = trans->conn_alloc(conn, gfp);

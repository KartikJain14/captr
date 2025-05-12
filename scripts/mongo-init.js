db.createUser({
	user: process.env.CAPTR_ADMIN_USERNAME,
	pwd: process.env.CAPTR_ADMIN_PASSWORD,
	roles: [
		{
			role: "readWrite",
			db: process.env.MONGO_INITDB_DATABASE,
		},
	],
});

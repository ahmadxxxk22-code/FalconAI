    # ==========================
    # API Keys
    # ==========================

    @staticmethod
    def save_api_key(
        db: Session,
        **kwargs
    ):

        api = ApiKey(**kwargs)

        db.add(api)

        db.commit()

        db.refresh(api)

        return api

    @staticmethod
    def get_api_keys(
        db: Session,
        user_id: int
    ):

        return db.query(
            ApiKey
        ).filter(
            ApiKey.user_id == user_id
        ).all()

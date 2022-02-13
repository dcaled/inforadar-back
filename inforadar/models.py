from inforadar.config import db, ma


class ErcSource(db.Model):
    __tablename__ = "erc_sources"
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.Integer)
    registration_date = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    periodicity = db.Column(db.String(50))
    support = db.Column(db.String(50))
    content_type = db.Column(db.String(255))
    geographic_scope = db.Column(db.String(50))
    director = db.Column(db.String(50))
    owner = db.Column(db.String(255))
    editor = db.Column(db.String(255))
    district = db.Column(db.String(50))
    municipality = db.Column(db.String(50))
    office_address = db.Column(db.String(255))
    location = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    institutional_email = db.Column(db.String(50))
    website = db.Column(db.String(255))
    domain = db.Column(db.String(50))
    last_update = db.Column(db.DateTime, nullable=False)


class ErcSourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ErcSource
        load_instance = True


class UserFeedback(db.Model):
    __tablename__ = "user_feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=0, nullable=False)
    crowdsourced_article_id = db.Column(db.Integer, db.ForeignKey('crowdsourced_articles.id'), nullable=False)
    indicator_version = db.Column(db.Integer, nullable=False)
    suggested_category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    main_category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)


class UserFeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserFeedback
        load_instance = True


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True


class Metric(db.Model):
    __tablename__ = "metrics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)


class MetricSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Metric
        load_instance = True


class Indicator(db.Model):
    __tablename__ = "indicators"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)


class IndicatorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Indicator
        load_instance = True


class CorpusMetricQuartile(db.Model):
    __tablename__ = "corpus_metrics_quartiles"
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('metrics.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    first_quartile = db.Column(db.Float, nullable=False)
    second_quartile = db.Column(db.Float, nullable=False)
    third_quartile = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('metric_id', 'category_id'),
    )


class CorpusMetricQuartileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CorpusMetricQuartile
        load_instance = True


class CorpusIndicatorQuartile(db.Model):
    __tablename__ = "corpus_indicators_quartiles"
    id = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    first_quartile = db.Column(db.Float, nullable=False)
    second_quartile = db.Column(db.Float, nullable=False)
    third_quartile = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('indicator_id', 'category_id'),
    )


class CorpusIndicatorQuartileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CorpusIndicatorQuartile
        load_instance = True


class CrowdsourcedArticle(db.Model):
    __tablename__ = "crowdsourced_articles"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    headline = db.Column(db.String(255), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    top_image = db.Column(db.String(255), nullable=True)
    source = db.Column(db.String(50), nullable=True)
    publish_date = db.Column(db.DateTime, nullable=True)
    creation_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=True)
    erc_registered = db.Column(db.Boolean, nullable=True)


class CrowdsourcedArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CrowdsourcedArticle
        load_instance = True


class CrowdsourcedMetricScore(db.Model):
    __tablename__ = "crowdsourced_metrics_scores"
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('metrics.id'), nullable=False)
    crowdsourced_article_id = db.Column(db.Integer, db.ForeignKey('crowdsourced_articles.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('metric_id', 'crowdsourced_article_id'),
    )


class CrowdsourcedMetricScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CrowdsourcedMetricScore
        load_instance = True


class CrowdsourcedIndicatorScore(db.Model):
    __tablename__ = "crowdsourced_indicators_scores"
    id = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)
    crowdsourced_article_id = db.Column(db.Integer, db.ForeignKey('crowdsourced_articles.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('indicator_id', 'crowdsourced_article_id', 'category_id'),
    )


class CrowdsourcedIndicatorScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CrowdsourcedIndicatorScore
        load_instance = True


class CorpusArticle(db.Model):
    __tablename__ = "corpus_articles"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(255), unique=True, nullable=True)
    headline = db.Column(db.String(255), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    top_image = db.Column(db.String(255), nullable=True)
    publish_date = db.Column(db.DateTime, nullable=False)
    filename = db.Column(db.String(255), nullable=False)


class CorpusArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CorpusArticle
        load_instance = True


class CorpusMetricScore(db.Model):
    __tablename__ = "corpus_metrics_scores"
    id = db.Column(db.Integer, primary_key=True)
    corpus_article_id = db.Column(db.Integer, db.ForeignKey('corpus_articles.id'), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey('metrics.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('corpus_article_id', 'metric_id'),
    )


class CorpusMetricScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CorpusMetricScore
        load_instance = True


# TODO: rever.
class CorpusIndicatorScore(db.Model):
    __tablename__ = "corpus_indicators_scores"
    id = db.Column(db.Integer, primary_key=True)
    corpus_article_id = db.Column(db.Integer, db.ForeignKey('corpus_articles.id'), nullable=False)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('corpus_article_id', 'indicator_id'),
    )


# TODO: rever.
class CorpusIndicatorScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CorpusIndicatorScore
        load_instance = True


class MetricPercentile(db.Model):
    __tablename__ = "metrics_percentiles"
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('metrics.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    corpus_metric_score_id = db.Column(db.Integer, db.ForeignKey('corpus_metrics_scores.id'), nullable=False)
    percentile = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('metric_id', 'category_id', 'corpus_metric_score_id'),
    )


class MetricPercentileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MetricPercentile
        load_instance = True


class IndicatorPercentile(db.Model):
    __tablename__ = "indicators_percentiles"
    id = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    corpus_indicator_score_id = db.Column(db.Integer, db.ForeignKey('corpus_indicators_scores.id'), nullable=False)
    percentile = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('indicator_id', 'category_id', 'corpus_indicator_score_id'),
    )


class IndicatorPercentileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IndicatorPercentile
        load_instance = True

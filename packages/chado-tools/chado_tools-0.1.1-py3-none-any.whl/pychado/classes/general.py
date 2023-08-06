import sqlalchemy.orm
from pychado.classes.base import Base

# Object-relational mappings for the CHADO General module


class Db(Base):
    """Class for the CHADO 'db' table"""
    # Columns
    db_id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=True)
    urlprefix = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=True)
    url = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=True)

    # Constraints
    __tablename__ = "db"
    __table_args__ = (sqlalchemy.UniqueConstraint(name, name="db_c1"), )

    # Initialisation
    def __init__(self, name, description=None, urlprefix=None, url=None, db_id=None):
        for key, value in locals().items():
            if key != self:
                setattr(self, key, value)



class DbxRef(Base):
    """Class for the CHADO 'dbxref' table"""
    # Columns
    dbxref_id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False, primary_key=True, autoincrement=True)
    db_id = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey(
        Db.db_id, onupdate="CASCADE", ondelete="CASCADE", deferrable=True, initially="DEFERRED"), nullable=False)
    accession = sqlalchemy.Column(sqlalchemy.VARCHAR(1024), nullable=False)
    version = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False, server_default=sqlalchemy.text("''"))
    description = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)

    # Db.dbxref = sqlalchemy.orm.relationship("DbxRef", back_populates=Db.__tablename__)
    # cvterm = sqlalchemy.orm.relationship("CvTerm", back_populates=__tablename__)

    # Constraints
    __tablename__ = "dbxref"
    __table_args__ = (sqlalchemy.UniqueConstraint(db_id, accession, version, name="dbxref_c1"),
                      sqlalchemy.Index("dbxref_idx1", db_id),
                      sqlalchemy.Index("dbxref_idx2", accession),
                      sqlalchemy.Index("dbxref_idx3", version))

    # Relationships
    db = sqlalchemy.orm.relationship(Db, backref=__tablename__)

    # Initialisation
    def __init__(self, accession, version="", description=None, dbxref_id=None, db_id=None):
        for key, value in locals().items():
            if key != self:
                setattr(self, key, value)

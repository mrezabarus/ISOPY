"""Cascade id dosen

Revision ID: 4e338d9794c5
Revises: a8aeccf94db6
Create Date: 2021-01-19 03:03:29.702226

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4e338d9794c5'
down_revision = 'a8aeccf94db6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dosen', 'alamat',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('dosen', 'nama',
               existing_type=mysql.VARCHAR(length=250),
               nullable=False)
    op.alter_column('dosen', 'nidn',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.alter_column('dosen', 'phone',
               existing_type=mysql.VARCHAR(length=13),
               nullable=False)
    op.drop_constraint('mahasiswa_ibfk_2', 'mahasiswa', type_='foreignkey')
    op.drop_constraint('mahasiswa_ibfk_1', 'mahasiswa', type_='foreignkey')
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_dua'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'mahasiswa', 'dosen', ['dosen_satu'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.drop_constraint(None, 'mahasiswa', type_='foreignkey')
    op.create_foreign_key('mahasiswa_ibfk_1', 'mahasiswa', 'dosen', ['dosen_dua'], ['id'])
    op.create_foreign_key('mahasiswa_ibfk_2', 'mahasiswa', 'dosen', ['dosen_satu'], ['id'])
    op.alter_column('dosen', 'phone',
               existing_type=mysql.VARCHAR(length=13),
               nullable=True)
    op.alter_column('dosen', 'nidn',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    op.alter_column('dosen', 'nama',
               existing_type=mysql.VARCHAR(length=250),
               nullable=True)
    op.alter_column('dosen', 'alamat',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###

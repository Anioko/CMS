"""empty message

Revision ID: d023c1d48e0e
Revises: eca5af8e2ef9
Create Date: 2020-05-02 20:44:17.115051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd023c1d48e0e'
down_revision = 'eca5af8e2ef9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogposts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('blogcategory_id', sa.Integer(), nullable=True),
    sa.Column('blogpoststatus_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('published_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['blogcategory_id'], ['blogcategories.id'], ),
    sa.ForeignKeyConstraint(['blogpoststatus_id'], ['blogpoststatus.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blogposts_slug'), 'blogposts', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blogposts_slug'), table_name='blogposts')
    op.drop_table('blogposts')
    # ### end Alembic commands ###
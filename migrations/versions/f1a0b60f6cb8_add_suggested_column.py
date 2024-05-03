"""add suggested column

Revision ID: f1a0b60f6cb8
Revises: 69bea51a93b0
Create Date: 2024-05-03 15:49:20.511980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a0b60f6cb8'
down_revision = '69bea51a93b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('score_table')
    op.drop_table('user')
    op.drop_table('wordle_puzzle')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wordle_puzzle',
    sa.Column('puzzle_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('puzzle_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('puzzle_solution', sa.VARCHAR(length=64), nullable=True),
    sa.Column('number_of_attempt', sa.INTEGER(), nullable=True),
    sa.Column('puzzle_score', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('puzzle_id'),
    sa.UniqueConstraint('puzzle_name')
    )
    op.create_table('user',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('overall_score', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('score_table',
    sa.Column('score_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('puzzle_id', sa.INTEGER(), nullable=False),
    sa.Column('score_achieved', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['puzzle_id'], ['wordle_puzzle.puzzle_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('score_id')
    )
    op.create_table('comments',
    sa.Column('comment_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('comment_text', sa.VARCHAR(length=256), nullable=True),
    sa.Column('posted_date', sa.DATETIME(), nullable=True),
    sa.Column('puzzle_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['puzzle_id'], ['wordle_puzzle.puzzle_id'], name='fk_comment_puzzle_id_wordle_puzzle', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    # ### end Alembic commands ###
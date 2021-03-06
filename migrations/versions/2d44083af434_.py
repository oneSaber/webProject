"""empty message

Revision ID: 2d44083af434
Revises: 
Create Date: 2019-05-23 22:34:33.995593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d44083af434'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('role', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account'),
    sa.UniqueConstraint('email')
    )
    op.create_table('choosecourses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('course_status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('commenter_id', sa.Integer(), nullable=False),
    sa.Column('commented_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('comment_type', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account'),
    sa.UniqueConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_name', sa.String(length=32), nullable=True),
    sa.Column('course_status', sa.Integer(), nullable=True),
    sa.Column('course_begin_date', sa.DATETIME(), nullable=True),
    sa.Column('course_time', sa.String(length=32), nullable=True),
    sa.Column('course_last_time', sa.Integer(), nullable=True),
    sa.Column('course_interval', sa.Integer(), nullable=True),
    sa.Column('course_total_times', sa.Integer(), nullable=True),
    sa.Column('number_had_finish', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('course_type_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('course_name')
    )
    op.create_table('coursetypies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=32), nullable=True),
    sa.Column('parent_type_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('reports',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reporter', sa.Integer(), nullable=False),
    sa.Column('reported', sa.Integer(), nullable=False),
    sa.Column('report_type', sa.Integer(), nullable=False),
    sa.Column('report_result', sa.TEXT(), nullable=False),
    sa.Column('admin', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('role', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('school', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account'),
    sa.UniqueConstraint('email')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('role', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teachers')
    op.drop_table('students')
    op.drop_table('reports')
    op.drop_table('coursetypies')
    op.drop_table('courses')
    op.drop_table('companies')
    op.drop_table('comments')
    op.drop_table('choosecourses')
    op.drop_table('admin')
    # ### end Alembic commands ###

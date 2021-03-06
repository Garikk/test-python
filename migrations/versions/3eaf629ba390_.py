"""empty message

Revision ID: 3eaf629ba390
Revises: 
Create Date: 2019-03-24 09:07:45.571867

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3eaf629ba390'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_type',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('liter_per_km', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('fuel_types',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('gas_stations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('car_user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('car_id', sa.Integer(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['car_id'], ['car_type.id'], onupdate='CASCADE', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('gas_stations_fuel',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('station_id', sa.Integer(), nullable=True),
                    sa.Column('fuel_id', sa.Integer(), nullable=True),
                    sa.Column('cost', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['fuel_id'], ['fuel_types.id'], onupdate='CASCADE', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['station_id'], ['gas_stations.id'], onupdate='CASCADE',
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gas_stations_fuel')
    op.drop_table('car_user')
    op.drop_table('user')
    op.drop_table('gas_stations')
    op.drop_table('fuel_types')
    op.drop_table('car_type')
    # ### end Alembic commands ###

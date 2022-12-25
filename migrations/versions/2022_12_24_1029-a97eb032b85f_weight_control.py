"""weight_control

Revision ID: a97eb032b85f
Revises: 493173b35ec8
Create Date: 2022-12-24 10:29:25.946592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a97eb032b85f'
down_revision = '493173b35ec8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        '''
        CREATE FUNCTION check_weight()
        RETURNS trigger AS $BODY$

        BEGIN
        IF NEW.count > 1000 THEN
            RAISE EXCEPTION 'Weight exception';
        END IF;
        RETURN NEW;
        END;
        $BODY$
        LANGUAGE 'plpgsql';
        '''
    )
    op.execute(
        '''
        CREATE TRIGGER verify_weight BEFORE INSERT OR UPDATE ON public.item
        FOR EACH ROW EXECUTE PROCEDURE check_weight();
        '''
    )


def downgrade() -> None:
    op.execute(
        '''
        DROP TRIGGER verify_weight ON public.item;
        '''
    )
    op.execute(
        '''
        DROP FUNCTION check_weight();
        '''
    )

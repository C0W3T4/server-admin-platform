from sqlalchemy import func


def get_count(query, column):
    count_q = query.statement.with_only_columns(
        [func.count(column)]).order_by(None)
    count = query.session.execute(count_q).scalar()
    return count

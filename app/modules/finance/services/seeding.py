from app.modules.finance.models.category import Categories, CategoryType

from app.core.database import get_database


def seed_categories():
    """Seed the categories table with default categories."""
    db = get_database()
    session = db.get_session()

    try:
        categories_data = [
            {"name": "Alimentação", "category_type": CategoryType.EXPENSE},
            {"name": "Transporte", "category_type": CategoryType.EXPENSE},
            {"name": "Entreterimento", "category_type": CategoryType.EXPENSE},
            {"name": "Saúde", "category_type": CategoryType.EXPENSE},
            {"name": "Educação", "category_type": CategoryType.EXPENSE},
            {"name": "Salário", "category_type": CategoryType.INCOME},
            {"name": "Freelance", "category_type": CategoryType.INCOME},
            {"name": "Investimentos", "category_type": CategoryType.INCOME},
            {"name": "Presentes", "category_type": CategoryType.INCOME},
        ]

        for category_data in categories_data:
            existing = session.query(Categories).filter_by(
                name=category_data["name"]
            ).first()

            if not existing:
                category = Categories(
                    name=category_data["name"],
                    category_type=category_data["category_type"],
                    parent_id=None,
                    is_active=True,
                )
                session.add(category)

        session.commit()
        print("Categories seeded successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error seeding categories: {e}")
    finally:
        session.close()

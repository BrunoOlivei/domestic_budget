from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.finance.models.category import Categories, CategoryType
from app.modules.finance.schemas.category import CategoryCreate


class CategoryService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def check_existing_category(self, name: str) -> bool:
        """
        Check if a category with the given name already exists.

        Args:
            name (str): The name of the category to check.

        Returns:
            bool: True if the category exists, False otherwise.
        """
        existing_category = (
            self.db_session.query(Categories).filter(Categories.name == name).first()
        )
        return existing_category is not None

    def get_category_by_id(self, category_id: int) -> Optional[Categories]:
        """
        Retrieve a category by its ID.

        Args:
            category_id (int): The ID of the category to retrieve.

        Returns:
            Optional[Categories]: The category record if found, else None.
        """
        category = (
            self.db_session.query(Categories)
            .filter(Categories.id == category_id)
            .first()
        )
        if not category:
            raise KeyError("Category not found")
        return category

    def get_categories(self) -> List[Categories]:
        """
        List all categories.

        Returns:
            List[Categories]: A list of all category records.
        """
        return self.db_session.query(Categories).all()

    def create_category(self, category_data: CategoryCreate) -> Categories:
        """
        Create a new category if doesn't exist a category with the same name
        If a parent_id is provided, ensure the parent category exists
        and matches the category_type. If the parent category's type differs, inherit its type.

        Args:
            category_data (CategoryCreate): The data for the new category.

        Returns:
            Categories: The newly created category record.
        """
        if self.check_existing_category(category_data.name):
            raise ValueError("Category with this name already exists")

        if category_data.parent_id is not None:
            category_father = self.get_category_by_id(category_data.parent_id)
            if category_father:
                if category_father.category_type != category_data.category_type:
                    category_data.category_type = CategoryType(category_father.category_type.lower())  # type: ignore
            else:
                raise KeyError("Parent category not found")

        new_category = Categories(**category_data.model_dump())

        self.db_session.add(new_category)
        self.db_session.commit()
        self.db_session.refresh(new_category)

        return new_category

from views import Index, About, CoursesList, CreateCourse, CategoryList, CopyCourse, CreateCategory

routes = {
    '/': Index(),
    '/about/': About(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse()
}

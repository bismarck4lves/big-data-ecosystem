from app import ma


class CompanySchema(ma.Schema):

    class Meta:
        fields = ('id', 'name')


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

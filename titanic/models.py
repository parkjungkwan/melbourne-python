from icecream import ic

from context.domains import Dataset
from context.models import Model


class TitanicModel(object):

    model = Model()
    dataset = Dataset()

    def preprocess(self, train_fname, test_fname):
        this = self.dataset
        that = self.model
        feature = ['PassengerId','Survived','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked']
        # 데이터셋은 Train, Test, Validation 3종류로 나뉜다
        this.train = that.new_dframe(train_fname)
        this.test = that.new_dframe(test_fname)
        this.id = this.test['PassengerId']
        this.label = this.train['Survived']
        this.train = this.train.drop('Survived', axis=1)
        # Entity 에서 Object 로 전환
        this = self.drop_feature(this, 'SibSp','Parch','Ticket','Cabin')
        # self.kwargs_sample(name='이순신') kwargs 샘플... 타이타닉 흐름과 무관
        this = self.extract_title_from_name(this)
        title_mapping = self.remove_duplicate(this)
        this = self.title_nominal(this, title_mapping)
        this = self.drop_feature(this,'Name')
        this = self.sex_nominal(this)
        this = self.drop_feature(this, 'Sex')
        '''
        
        this = self.age_ratio(this)
        this = self.embarked_nominal(this)
        this = self.pclass_ordinal(this)
        this = self.fare_ratio(this)
        '''

        self.df_info(this)
        return this

    @staticmethod
    def df_info(this):
        [print(f'{i.info()}') for i in [this.train, this.test]]
        ic(this.train.head(3))
        ic(this.test.head(3))

    @staticmethod
    def null_check(this):
        [ic(f'{i.isnull().sum()}') for i in [this.train, this.test]]

    @staticmethod
    def id_info(this):
        ic(f'id 의 타입  {type(this.id)}')
        ic(f'id 의 상위 3개 {this.id[:3]}')

    @staticmethod
    def drop_feature(this, *feature) -> object:
        # ic(type(feature)) # ic| type(feature): <class 'tuple'>
        '''
        for i in [this.train, this.test]:
            for j in feature:
                i.drop(j, axis=1, inplace=True)'''
        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train, this.test]]
        return this

    @staticmethod
    def kwargs_sample(**kwargs) -> None:
        # ic(type(kwargs))
        {print(''.join(f'key:{i}, val:{j}')) for i, j in kwargs.items()} # key:name, val:이순신

    '''
    Categorical vs. Quantitative
    Cate -> nominal (이름) vs. ordinal (순서)
    Quan -> interval (상대) vs. ratio (절대)
    '''

    @staticmethod
    def pclass_ordinal(this)->object:
        return this

    @staticmethod
    def extract_title_from_name(this) -> None:
        for these in [this.train, this.test]:
            these['Title'] = these.Name.str.extract('([A-Za-z]+)\.', expand=False)
        # ic(this.train.head(5))
        return this

    @staticmethod
    def remove_duplicate(this) -> None:
        a = []
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        # print(f'>>> {a}')
        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        title_mapping = {'Mr': 1, 'Ms': 2, 'Mrs':3, 'Master':4, 'Royal':5, 'Rare': 6}
        return title_mapping

    @staticmethod
    def title_nominal(this, title_mapping) -> object:
        for these in [this.train, this.test]:
            these['Title'] = these['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            these['Title'] = these['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 'Rare')
            these['Title'] = these['Title'].replace(['Mlle'], 'Mr')
            these['Title'] = these['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            these['Title'] = these['Title'].fillna(0)
            these['Title'] = these['Title'].map(title_mapping)
        return this

    @staticmethod
    def age_ratio(this) -> object:

        return this

    @staticmethod
    def sex_nominal(this)->object:
        for these in [this.train, this.test]:
            gender_mapping = {'male':0, 'female':1}
            these['Gender'] = these['Sex'].map(gender_mapping)
        return this

    @staticmethod
    def embarked_nominal(this) -> object:
        embarked_mapping = {'S': 1, 'C': 2, 'Q':3}
        this.train = this.train.fillna({'Embarked':'S'})
        return this

    @staticmethod
    def fare_ratio(this) -> object:
        return this



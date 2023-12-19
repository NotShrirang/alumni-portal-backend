from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_feed_recommendation(qs, user):
    """
    qs: Queryset of Feed objects
    user: Current user
    """

    # Get all feed objects
    feed_objects = qs.all()

    if qs.count() == 0:
        return feed_objects, []

    # Get all feed subjects
    feed_subjects_body = [" ".join(feed.subject.split(";"))+feed.body for feed in feed_objects]

    liked_feed_objects = feed_objects.filter(id__in=user.feed_actions.all().values_list('feed', flat=True))

    if liked_feed_objects.count() == 0:
        return feed_objects, []

    # Get all feed subjects of current user
    liked_feed_subjects_body = [" ".join(feed.subject.split(";"))+feed.body for feed in liked_feed_objects]

    # Initialize TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform feed subjects
    feed_subjects_body_vector = vectorizer.fit_transform(feed_subjects_body)

    # Transform user feed subjects
    liked_feed_subjects_body_vector = vectorizer.transform(liked_feed_subjects_body)

    # Get similarity score
    similarity_score = cosine_similarity(liked_feed_subjects_body_vector, feed_subjects_body_vector)

    # Get indices of feed objects
    feed_indices = [i for i in range(len(feed_objects))]

    # Get indices of feed objects in descending order of similarity score
    feed_indices = [x for _, x in sorted(zip(similarity_score[0], feed_indices), reverse=True)]

    # Get similarity score in descending order
    similarity_score = sorted(similarity_score[0], reverse=True)

    # Get feed objects in descending order of similarity score
    feed_objects = [feed_objects[i] for i in feed_indices]

    return feed_objects, similarity_score

def get_user_recommendation(qs, current_user):
    """
    qs: Queryset of User objects
    current_user: Current user
    """

    # Get all user objects
    user_objects = qs.all()

    if qs.count() == 0:
        return user_objects, []

    # Get all user attributes
    user_attributes = [user.firstName + user.lastName + user.department + user.email for user in user_objects]

    # Get attributes of the current user
    current_user_attributes = [current_user.firstName + current_user.lastName + current_user.department + current_user.email]

    # Initialize TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform user attributes
    user_attributes_vector = vectorizer.fit_transform(user_attributes)

    # Transform current user attributes
    current_user_attributes_vector = vectorizer.transform(current_user_attributes)

    # Get similarity score
    similarity_score = cosine_similarity(current_user_attributes_vector, user_attributes_vector)

    # Get indices of user objects
    user_indices = [i for i in range(len(user_objects))]

    # Get indices of user objects in descending order of similarity score
    user_indices = [x for _, x in sorted(zip(similarity_score[0], user_indices), reverse=True)]

    # Get similarity score in descending order
    similarity_score = sorted(similarity_score[0], reverse=True)

    # Get user objects in descending order of similarity score
    user_objects = [user_objects[i] for i in user_indices]

    return user_objects, similarity_score